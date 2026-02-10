"""Core types - Messages, Events, Intents, Tool calls."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Callable, Awaitable, Literal, NotRequired, TypedDict
from uuid import uuid4


class ToolCallFunction(TypedDict):
    name: str
    arguments: str


class ToolCallDict(TypedDict):
    id: str
    type: Literal["function"]
    function: ToolCallFunction


class UserMessage(TypedDict):
    role: Literal["user"]
    content: str


class AssistantMessage(TypedDict, total=False):
    role: Literal["assistant"]  # Required
    content: str | None
    tool_calls: list[ToolCallDict]


class ToolMessage(TypedDict):
    role: Literal["tool"]
    tool_call_id: str
    content: str


Message = UserMessage | AssistantMessage | ToolMessage


@dataclass
class ToolCall:
    """Parsed tool call from LLM response."""

    id: str
    name: str
    args: dict = field(default_factory=dict)

    def to_dict(self) -> ToolCallDict:
        import json

        return {
            "id": self.id,
            "type": "function",
            "function": {"name": self.name, "arguments": json.dumps(self.args)},
        }


@dataclass
class ToolResult:
    """Result of tool execution."""

    id: str
    name: str
    output: str = ""
    error: str = ""

    @property
    def success(self) -> bool:
        return not self.error

    def to_message(self) -> ToolMessage:
        return {
            "role": "tool",
            "tool_call_id": self.id,
            "content": self.output or self.error,
        }


@dataclass
class Response:
    """LLM response."""

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def done(self) -> bool:
        return len(self.tool_calls) == 0

    def to_message(self) -> AssistantMessage:
        msg: AssistantMessage = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            msg["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]
        return msg


@dataclass
class Done:
    """Agent completed its task."""

    output: str


@dataclass
class Handoff:
    """Agent wants to delegate to another agent."""

    agent: str
    task: str


@dataclass
class HumanInput:
    """Agent needs human input to proceed."""

    prompt: str
    timeout: int | None = None


@dataclass
class Continue:
    """Agent should continue its loop (internal use)."""

    pass


Intent = Done | Handoff | HumanInput | Continue


class EventType(StrEnum):
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"

    AGENT_START = "agent_start"
    AGENT_END = "agent_end"

    LLM_START = "llm_start"
    LLM_STREAM_START = "llm_stream_start"
    LLM_STREAM_CHUNK = "llm_stream_chunk"
    LLM_END = "llm_end"

    TOOL_START = "tool_start"
    TOOL_END = "tool_end"

    DELEGATION_START = "delegation_start"
    DELEGATION_END = "delegation_end"

    HUMAN_INPUT_WAITING = "human_input_waiting"
    HUMAN_INPUT_RECEIVED = "human_input_received"

    APPROVAL_REQUIRED = "approval_required"
    TOOL_DENIED = "tool_denied"

    ENVIRONMENT_INFO = "environment_info"


class WorkflowStartData(TypedDict):
    task: str


class WorkflowEndData(TypedDict):
    output: str
    total_turns: int


class AgentStartData(TypedDict):
    task: str


class AgentEndData(TypedDict):
    output: str
    turns: int


class LLMStartData(TypedDict):
    turn: int
    messages: int


class LLMEndData(TypedDict):
    content: str
    tool_calls: int
    tokens: int


class ToolStartData(TypedDict):
    name: str
    args: dict


class ToolEndData(TypedDict):
    name: str
    success: bool
    duration_ms: int
    error: NotRequired[str]


class DelegationStartData(TypedDict):
    agent: str
    task: str


class DelegationEndData(TypedDict):
    result: str


class HumanInputWaitingData(TypedDict):
    prompt: str


class HumanInputReceivedData(TypedDict):
    response: str


class ApprovalRequiredData(TypedDict):
    tool: str
    args: dict
    request_id: NotRequired[str]


class ToolDeniedData(TypedDict):
    tool: str


EventData = (
    WorkflowStartData
    | WorkflowEndData
    | AgentStartData
    | AgentEndData
    | LLMStartData
    | LLMEndData
    | ToolStartData
    | ToolEndData
    | DelegationStartData
    | DelegationEndData
    | HumanInputWaitingData
    | HumanInputReceivedData
    | ApprovalRequiredData
    | ToolDeniedData
    | dict
)


@dataclass(frozen=True)
class Span:
    """Identifies event source. Tracks parent-child for delegation."""

    run_id: str = field(default_factory=lambda: uuid4().hex[:8])
    agent: str = "main"
    depth: int = 0
    parent_run_id: str | None = None

    def child(self, agent: str) -> "Span":
        return Span(
            run_id=uuid4().hex[:8],
            agent=agent,
            depth=self.depth + 1,
            parent_run_id=self.run_id,
        )


@dataclass
class Event:
    """Typed event for SDK/TUI consumption."""

    type: EventType
    span: Span
    data: EventData = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "span": {
                "run_id": self.span.run_id,
                "agent": self.span.agent,
                "depth": self.span.depth,
                "parent_run_id": self.span.parent_run_id,
            },
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentRole(StrEnum):
    """Explicit role for an agent."""

    MAIN = "main"
    SUBAGENT = "subagent"
    WORKER = "worker"


@dataclass
class AgentConfig:
    """Configuration for an agent type."""

    name: str
    system_prompt: str
    role: AgentRole = AgentRole.MAIN
    allowed_tools: list[str] = field(default_factory=list)
    max_turns: int = 20

    _can_delegate: bool | None = None
    _can_be_delegated_to: bool | None = None

    @property
    def can_delegate(self) -> bool:
        """Can this agent delegate to other agents?"""
        if self._can_delegate is not None:
            return self._can_delegate
        return self.role == AgentRole.MAIN

    @property
    def can_be_delegated_to(self) -> bool:
        """Can other agents delegate to this one?"""
        if self._can_be_delegated_to is not None:
            return self._can_be_delegated_to
        return self.role in (AgentRole.SUBAGENT, AgentRole.WORKER)

    @property
    def supports_multi_turn(self) -> bool:
        """Does this agent support continue_with()?"""
        return self.role == AgentRole.MAIN


ApprovalFn = Callable[[str, dict], Awaitable[bool]]
HumanInputFn = Callable[[str], Awaitable[str]]
EventHandler = Callable[[Event], None]
