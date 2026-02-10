"""The Agent. Pure ReAct loop. Returns intents for Runner to interpret."""

from .models import (
    AgentConfig, Message, UserMessage, Response, EventType,
    Intent, Done, Handoff, HumanInput, Continue,
    AgentStartData, AgentEndData, LLMStartData, LLMEndData,
)
from .events import Emitter
from .tools import ToolRunner
from .llm import LLM


class Agent:
    
    def __init__(
        self,
        llm: LLM,
        tools: ToolRunner,
        config: AgentConfig,
        emitter: Emitter | None = None,
    ):
        self.llm = llm
        self.tools = tools
        self.config = config
        self.emitter = emitter or Emitter.null()
        self.messages: list[Message] = []
        self._turn = 0
    
    def set_task(self, task: str) -> None:
        self.messages = [UserMessage(role="user", content=task)]
        self._turn = 0
        self.emitter.emit(EventType.AGENT_START, AgentStartData(task=task[:200]))
    
    def add_result(self, result: str) -> None:
        # External results (tool outputs/subagent results) injected as user messages
        self.messages.append(UserMessage(role="user", content=result))
    
    async def step(self) -> Intent:
        if self._turn >= self.config.max_turns:
            self.emitter.emit(EventType.AGENT_END, AgentEndData(output="max_turns", turns=self._turn))
            last = self.messages[-1] if self.messages else {}
            return Done(last.get("content", "") if isinstance(last, dict) else "")
        

        self.emitter.emit(EventType.LLM_START, LLMStartData(turn=self._turn, messages=len(self.messages)))
        
        response = None
        has_streamed = False
        

        if hasattr(self.llm, 'complete_stream'):
            self.emitter.emit(EventType.LLM_STREAM_START, {})
            
            async for chunk in self.llm.complete_stream(
                self.messages,  # type: ignore
                self.tools.schemas(self.config.allowed_tools),
                self.config.system_prompt,
            ):
                if isinstance(chunk, str):
                    self.emitter.emit(EventType.LLM_STREAM_CHUNK, {"content": chunk})
                    has_streamed = True
                else:
                    response = chunk
        else:
            response = await self.llm.complete(
                self.messages,  # type: ignore
                self.tools.schemas(self.config.allowed_tools),
                self.config.system_prompt,
            )
        
        self.emitter.emit(EventType.LLM_END, LLMEndData(
            content=response.content[:200] if response.content else "",
            tool_calls=len(response.tool_calls),
            tokens=response.input_tokens + response.output_tokens,
        ))
        
        self.messages.append(response.to_message())
        self._turn += 1
        

        if response.done:
            self.emitter.emit(EventType.AGENT_END, AgentEndData(
                output=response.content[:200],
                turns=self._turn,
            ))
            return Done(response.content)
        

        results = await self.tools.run_many(response.tool_calls, self.emitter)
        

        for result in results:
            if isinstance(result.output, Handoff):
                return result.output
            if isinstance(result.output, HumanInput):
                return result.output
        
        for result in results:
            self.messages.append(result.to_message())
        
        return Continue()
    
    async def run(self) -> str:
        while True:
            intent = await self.step()
            
            if isinstance(intent, Done):
                return intent.output
            elif isinstance(intent, Continue):
                continue
            else:
                raise RuntimeError(f"Agent returned {type(intent).__name__} but no Runner to handle it")
