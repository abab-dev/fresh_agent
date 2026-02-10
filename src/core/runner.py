"""Runner - Runs agents, handles intents, manages sessions."""

import asyncio

from .models import (
    EventType,
    Span,
    AgentConfig,
    AgentRole,
    Intent,
    Done,
    Handoff,
    HumanInput,
    Continue,
    WorkflowStartData,
    WorkflowEndData,
    DelegationStartData,
    DelegationEndData,
    HumanInputWaitingData,
    HumanInputReceivedData,
    HumanInputFn,
    EventHandler,
    UserMessage,
    ApprovalFn,
)
from .events import Emitter
from .agent import Agent
from .tools import Tool, ToolRunner
from .llm import LLM
from .delegation import DelegateTool


class Runner:
    """
    Runs agents. Handles intents. Manages sessions.

    Example:
        runner = Runner.create(
            llm=llm,
            tools=[read_file, edit_file, ripgrep],
            agents={
                "main": AgentConfig(
                    name="main",
                    role=AgentRole.MAIN,
                    system_prompt="You are a coding assistant.",
                    allowed_tools=["read_file", "edit_file", "delegate"],
                ),
                "explorer": AgentConfig(
                    name="explorer",
                    role=AgentRole.SUBAGENT,
                    system_prompt="You explore codebases.",
                    allowed_tools=["ripgrep", "read_file"],
                ),
            },
        )

        result = await runner.run("Fix the bug")
        result = await runner.continue_with("Also add tests")
    """

    def __init__(
        self,
        llm: LLM,
        tools: list[Tool],
        agents: dict[str, AgentConfig],
        handler: EventHandler | None = None,
        human_input_fn: HumanInputFn | None = None,
        approve: ApprovalFn | None = None,
    ):
        self.llm = llm
        self.tools = tools
        self.agents = agents
        self.handler = handler
        self.human_input_fn = human_input_fn
        self.approve = approve

        self._total_turns = 0
        self._agent: Agent | None = None
        self._emitter: Emitter | None = None

    @classmethod
    def create(
        cls,
        llm: LLM,
        tools: list[Tool],
        agents: dict[str, AgentConfig],
        handler: EventHandler | None = None,
        human_input_fn: HumanInputFn | None = None,
        approve: ApprovalFn | None = None,
    ) -> "Runner":
        return cls(
            llm=llm,
            tools=tools,
            agents=agents,
            handler=handler,
            human_input_fn=human_input_fn,
            approve=approve,
        )

    @property
    def has_session(self) -> bool:
        return self._agent is not None

    @property
    def registered_agents(self) -> list[str]:
        return list(self.agents.keys())

    @property
    def subagents(self) -> list[str]:
        return [name for name, cfg in self.agents.items() if cfg.can_be_delegated_to]

    @property
    def main_agents(self) -> list[str]:
        return [name for name, cfg in self.agents.items() if cfg.role == AgentRole.MAIN]

    def _create_agent(self, agent_type: str, emitter: Emitter) -> Agent:
        config = self.agents.get(agent_type)
        if not config:
            available = ", ".join(self.agents.keys())
            raise ValueError(f"Unknown agent: '{agent_type}'. Available: {available}")

        tools_list = list(self.tools)

        if config.can_delegate and "delegate" in config.allowed_tools:
            delegate_tool = DelegateTool()
            delegate_tool.available_agents = [
                name
                for name, cfg in self.agents.items()
                if cfg.can_be_delegated_to and name != agent_type
            ]
            tools_list.append(delegate_tool)

        allowed = set(config.allowed_tools)
        filtered = [t for t in tools_list if t.name in allowed]

        return Agent(
            llm=self.llm,
            tools=ToolRunner(filtered, self.approve),
            config=config,
            emitter=emitter,
        )

    async def run(self, task: str, agent_type: str = "main") -> str:
        config = self.agents.get(agent_type)
        if not config:
            raise ValueError(f"Unknown agent: '{agent_type}'")
        if config.role != AgentRole.MAIN:
            raise ValueError(
                f"Cannot start session with '{agent_type}' (role={config.role}). "
                f"Only MAIN agents can be entry points. Available: {self.main_agents}"
            )
        self._total_turns = 0
        span = Span(agent=agent_type)
        self._emitter = Emitter(self.handler, span)

        self._emitter.emit(EventType.WORKFLOW_START, WorkflowStartData(task=task[:200]))

        self._agent = self._create_agent(agent_type, self._emitter)
        self._agent.set_task(task)

        return await self._loop()

    async def continue_with(self, user_input: str) -> str:
        if not self._agent or not self._emitter:
            raise RuntimeError("No active session. Call run() first.")

        if not self._agent.config.supports_multi_turn:
            raise RuntimeError(
                f"Agent '{self._agent.config.name}' does not support multi-turn. "
                "Only MAIN agents support continue_with()."
            )

        self._agent.messages.append(UserMessage(role="user", content=user_input))
        self._emitter.emit(EventType.AGENT_START, {"task": user_input[:200]})

        return await self._loop()

    async def end_session(self) -> None:
        if self._emitter:
            self._emitter.emit(
                EventType.WORKFLOW_END,
                WorkflowEndData(
                    output="session_ended",
                    total_turns=self._total_turns,
                ),
            )
        self._agent = None
        self._emitter = None

    async def _loop(self) -> str:
        while True:
            intent = await self._agent.step()
            self._total_turns += 1

            match intent:
                case Done(output):
                    return output

                case Handoff(target_agent, subtask):
                    child_result = await self._handle_handoff(target_agent, subtask)
                    self._agent.add_result(f"[{target_agent} result]: {child_result}")

                case HumanInput(prompt, timeout):
                    result = await self._handle_human_input(prompt)
                    self._agent.add_result(result)

                case Continue():
                    continue

    async def _handle_handoff(self, agent_type: str, task: str) -> str:
        child_emitter = self._emitter.child(agent_type)
        child_emitter.emit(
            EventType.DELEGATION_START,
            DelegationStartData(agent=agent_type, task=task[:100]),
        )

        child_agent = self._create_agent(agent_type, child_emitter)
        child_agent.set_task(task)

        result = await self._run_child(child_agent, child_emitter)

        child_emitter.emit(
            EventType.DELEGATION_END,
            DelegationEndData(result=result[:200] if result else ""),
        )

        return result

    async def _run_child(self, agent: Agent, emitter: Emitter) -> str:
        while True:
            intent = await agent.step()
            self._total_turns += 1

            match intent:
                case Done(output):
                    return output
                case Handoff(target_agent, subtask):
                    child_result = await self._handle_handoff(target_agent, subtask)
                    agent.add_result(f"[{target_agent} result]: {child_result}")
                case HumanInput(prompt, _):
                    result = await self._handle_human_input(prompt)
                    agent.add_result(result)
                case Continue():
                    continue

    async def _handle_human_input(self, prompt: str) -> str:
        if not self.human_input_fn:
            return "[Error: No human input handler configured]"

        self._emitter.emit(
            EventType.HUMAN_INPUT_WAITING, HumanInputWaitingData(prompt=prompt)
        )
        response = await self.human_input_fn(prompt)
        self._emitter.emit(
            EventType.HUMAN_INPUT_RECEIVED,
            HumanInputReceivedData(response=response[:200]),
        )

        return response

    async def run_parallel(self, tasks: list[tuple[str, str]]) -> list[str]:
        """
        Run multiple agents in parallel.

        Args:
            tasks: List of (agent_type, task) tuples

        Returns:
            List of results in same order
        """

        async def run_one(agent_type: str, task: str) -> str:
            emitter = Emitter(self.handler, Span(agent=agent_type))
            agent = self._create_agent(agent_type, emitter)
            agent.set_task(task)
            while True:
                intent = await agent.step()
                if isinstance(intent, Done):
                    return intent.output
                elif isinstance(intent, Continue):
                    continue
                else:
                    raise RuntimeError(f"Parallel agents can't handle {type(intent)}")

        return await asyncio.gather(*[run_one(a, t) for a, t in tasks])

    async def run_pipeline(self, steps: list[tuple[str, str]]) -> str:
        """
        Run agents sequentially, chaining outputs.

        Args:
            steps: List of (agent_type, task_template) tuples

        Returns:
            Final result
        """
        result = ""
        for agent_type, task in steps:
            full_task = f"{task}\n\nPrevious result:\n{result}" if result else task
            emitter = Emitter(self.handler, Span(agent=agent_type))
            agent = self._create_agent(agent_type, emitter)
            agent.set_task(full_task)

            while True:
                intent = await agent.step()
                if isinstance(intent, Done):
                    result = intent.output
                    break
                elif isinstance(intent, Continue):
                    continue
                else:
                    raise RuntimeError(f"Pipeline agents can't handle {type(intent)}")

        return result
