"""Tool protocol and runner."""

import asyncio
import time
from typing import Any, Protocol, runtime_checkable

from .models import (
    ToolCall, ToolResult, ApprovalFn, EventType,
    ToolStartData, ToolEndData, Handoff, HumanInput,
)
from .events import Emitter


@runtime_checkable
class Tool(Protocol):
    name: str
    
    def schema(self) -> dict:
        ...
    
    async def execute(self, **kwargs) -> Any:
        ...


class ToolRunner:
    def __init__(self, tools: list[Tool], approve: ApprovalFn | None = None):
        self._tools = {t.name: t for t in tools}
        self._approve = approve
    
    def schemas(self, names: list[str] | None = None) -> list[dict]:
        if names is None:
            return [t.schema() for t in self._tools.values()]
        return [self._tools[n].schema() for n in names if n in self._tools]
    
    async def run(self, call: ToolCall, emitter: Emitter) -> ToolResult:
        tool = self._tools.get(call.name)
        if not tool:
            return ToolResult(call.id, call.name, error=f"Unknown tool: {call.name}")
        

        if hasattr(tool, 'needs_approval') and tool.needs_approval(**call.args):
            emitter.emit(EventType.APPROVAL_REQUIRED, {"tool": call.name, "args": call.args})
            if self._approve:
                approved = await self._approve(call.name, call.args)
                if not approved:
                    emitter.emit(EventType.TOOL_DENIED, {"tool": call.name})
                    return ToolResult(call.id, call.name, error="Denied by user")
        
        emitter.emit(EventType.TOOL_START, ToolStartData(name=call.name, args=call.args))
        start = time.perf_counter()
        
        try:
            result = await tool.execute(**call.args)
            duration = int((time.perf_counter() - start) * 1000)
            
            # Tools can return control flow (Handoff/HumanInput) instead of strings
            if isinstance(result, (Handoff, HumanInput)):
                emitter.emit(EventType.TOOL_END, ToolEndData(
                    name=call.name, success=True, duration_ms=duration
                ))
                return ToolResult(call.id, call.name, output=result)  # type: ignore
            
            emitter.emit(EventType.TOOL_END, ToolEndData(
                name=call.name, success=True, duration_ms=duration
            ))
            return ToolResult(call.id, call.name, output=str(result))
            
        except Exception as e:
            duration = int((time.perf_counter() - start) * 1000)
            emitter.emit(EventType.TOOL_END, ToolEndData(
                name=call.name, success=False, duration_ms=duration, error=str(e)
            ))
            return ToolResult(call.id, call.name, error=str(e))
    
    async def run_many(self, calls: list[ToolCall], emitter: Emitter) -> list[ToolResult]:
        return await asyncio.gather(*[self.run(c, emitter) for c in calls])


class LegacyToolAdapter:
    
    def __init__(self, legacy):
        self._legacy = legacy
        self.name = legacy.get_tool_name()
    
    def schema(self) -> dict:
        return self._legacy.json_schema()
    
    async def execute(self, **kwargs) -> Any:
        return await self._legacy.act(**kwargs)
    
    def needs_approval(self, **kwargs) -> bool:
        if hasattr(self._legacy, 'needs_approval'):
            return self._legacy.needs_approval(**kwargs)
        return False
