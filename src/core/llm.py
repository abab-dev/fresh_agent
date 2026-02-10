import os
import json
from typing import Protocol

from .models import ToolCall, Response


class LLM(Protocol):
    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        system: str | None = None,
    ) -> Response: ...


def get_model_from_env() -> str:
    model = os.getenv("MODEL_NAME", "gpt-4o")
    base_url = os.getenv("OPENAI_BASE_URL")

    if base_url and not model.startswith("openai/"):
        return f"openai/{model}"

    if not model.startswith(("openai/", "anthropic/", "azure/", "ollama/", "groq/")):
        model = f"openai/{model}"
    return model


class LiteLLMClient:
    def __init__(self, model: str | None = None):
        self.model = model or get_model_from_env()

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        system: str | None = None,
    ) -> Response:
        import litellm

        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        kwargs = {"model": self.model, "messages": all_messages}

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            kwargs["api_base"] = base_url

        response = await litellm.acompletion(**kwargs)
        return self._parse(response)

    async def complete_stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        system: str | None = None,
    ):
        import litellm

        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        kwargs = {"model": self.model, "messages": all_messages, "stream": True}

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            kwargs["api_base"] = base_url

        response_stream = await litellm.acompletion(**kwargs)

        # We need to accumulate the full response for the final return value.
        # This is especially tricky for tool calls, which come in fragmented chunks across multiple indices.
        content_chunks = []
        tool_calls_data = {}
        input_tokens = 0
        output_tokens = 0

        async for chunk in response_stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if not delta:
                continue

            if delta.content:
                content_chunks.append(delta.content)
                yield delta.content

            # Tool calls stream as fragments - need to accumulate and reassemble
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index if hasattr(tc, "index") else 0
                    if idx not in tool_calls_data:
                        tool_calls_data[idx] = {
                            "id": tc.id or "",
                            "name": "",
                            "args": "",
                        }
                    if tc.id:
                        tool_calls_data[idx]["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            tool_calls_data[idx]["name"] = tc.function.name
                        if tc.function.arguments:
                            tool_calls_data[idx]["args"] += tc.function.arguments

            if hasattr(chunk, "usage") and chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens

        tool_calls = []
        for tc_data in tool_calls_data.values():
            try:
                args = json.loads(tc_data["args"]) if tc_data["args"] else {}
            except json.JSONDecodeError:
                args = {}
            tool_calls.append(
                ToolCall(id=tc_data["id"], name=tc_data["name"], args=args)
            )

        yield Response(
            content="".join(content_chunks),
            tool_calls=tool_calls,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    def _parse(self, response) -> Response:
        message = response.choices[0].message

        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                args = tc.function.arguments
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                tool_calls.append(ToolCall(id=tc.id, name=tc.function.name, args=args))

        return Response(
            content=message.content or "",
            tool_calls=tool_calls,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )


class MockLLM:
    def __init__(self, responses: list[Response] | None = None):
        self.responses = responses or []
        self._idx = 0
        self.calls: list[dict] = []

    async def complete(
        self, messages: list, tools: list | None = None, system: str | None = None
    ) -> Response:
        self.calls.append({"messages": messages, "tools": tools, "system": system})
        if self._idx < len(self.responses):
            r = self.responses[self._idx]
            self._idx += 1
            return r
        return Response(content="Done.", tool_calls=[])

    async def complete_stream(
        self, messages: list, tools: list | None = None, system: str | None = None
    ):
        response = await self.complete(messages, tools, system)
        if response.content:
            for char in response.content:
                yield char
        yield response


def create_llm(model: str | None = None) -> LiteLLMClient:
    return LiteLLMClient(model)
