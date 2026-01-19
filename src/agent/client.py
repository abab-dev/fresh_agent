import logging
import time
from typing import Any, Dict, Generator, Tuple, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

from src.agent.config import AgentConfig
from src.utils.retry import is_retryable, retry_with_backoff

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
        self._total_cost = 0.0
    
    @property
    def total_cost(self) -> float:
        return round(self._total_cost, 4)
    
    def get_completion(self, request_params: Dict[str, Any]) -> Tuple[Any, Any]:
        request_params["model"] = self.config.model
        
        def make_request():
            response = self.client.chat.completions.create(**request_params)
            message = response.choices[0].message
            token_usage = response.usage
            self._update_cost(token_usage)
            return message, token_usage
        
        return retry_with_backoff(
            make_request,
            max_retries=self.config.max_retries,
            base_delay=self.config.base_delay,
            max_delay=self.config.max_delay,
            should_retry=is_retryable
        )
    
    def get_completion_stream(self, request_params: Dict[str, Any]) -> Generator[Any, None, None]:
        request_params["model"] = self.config.model
        request_params["stream"] = True
        request_params["stream_options"] = {"include_usage": True}
        
        last_error = None
        
        for attempt in range(self.config.max_retries):
            try:
                yield from self._stream_completion(request_params)
                return
                
            except Exception as e:
                last_error = e
                
                if not is_retryable(e) or attempt == self.config.max_retries - 1:
                    raise Exception(f"Streaming API request failed: {str(e)}")
                
                delay = self._calculate_delay(attempt)
                logger.warning(
                    f"Streaming request failed (attempt {attempt + 1}/{self.config.max_retries}): {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                time.sleep(delay)
        
        raise Exception(
            f"Streaming API request failed after {self.config.max_retries} retries: {str(last_error)}"
        )
    
    def _calculate_delay(self, attempt: int) -> float:
        delay = self.config.base_delay * (2 ** attempt)
        return min(delay, self.config.max_delay)
    
    def _update_cost(self, token_usage) -> None:
        if token_usage:
            cost = getattr(token_usage, 'model_extra', {})
            if isinstance(cost, dict):
                self._total_cost += cost.get("cost", 0)
    
    def _stream_completion(self, request_params: Dict[str, Any]) -> Generator[Any, None, None]:
        stream = self.client.chat.completions.create(**request_params)
        
        full_content = ""
        tool_calls = []
        token_usage = None
        
        for chunk in stream:
            if hasattr(chunk, 'usage') and chunk.usage:
                token_usage = chunk.usage
                self._update_cost(token_usage)
                continue
            
            if not chunk.choices:
                continue
                
            delta = chunk.choices[0].delta
            
            if delta.content:
                content_chunk = delta.content
                full_content += content_chunk
                yield content_chunk
            
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
                for tool_call_delta in delta.tool_calls:
                    if tool_call_delta.index is not None:
                        while len(tool_calls) <= tool_call_delta.index:
                            tool_calls.append({
                                'id': None,
                                'type': 'function',
                                'function': {'name': None, 'arguments': ''}
                            })
                        
                        current_tool_call = tool_calls[tool_call_delta.index]
                        
                        if tool_call_delta.id:
                            current_tool_call['id'] = tool_call_delta.id
                        
                        if tool_call_delta.function:
                            if tool_call_delta.function.name:
                                current_tool_call['function']['name'] = tool_call_delta.function.name
                            if tool_call_delta.function.arguments:
                                current_tool_call['function']['arguments'] += tool_call_delta.function.arguments
        
        formatted_tool_calls = None
        if tool_calls and any(tc['id'] for tc in tool_calls):
            formatted_tool_calls = []
            for tc in tool_calls:
                if tc['id'] and tc['function']['name']:
                    formatted_tool_calls.append(
                        ChatCompletionMessageToolCall(
                            id=tc['id'],
                            function=Function(
                                name=tc['function']['name'],
                                arguments=tc['function']['arguments']
                            ),
                            type='function'
                        )
                    )
        
        message = ChatCompletionMessage(
            content=full_content if full_content else None,
            role="assistant",
            tool_calls=formatted_tool_calls,
            refusal=None,
        )

        if token_usage:
            message.usage = token_usage
        
        yield message
