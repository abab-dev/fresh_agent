import sys
from datetime import datetime

from ..models import Event, EventType


class Logger:
    def __init__(self, verbose: bool = True, output=sys.stderr):
        self.verbose = verbose
        self.output = output

    def handle(self, event: Event) -> None:
        indent = "  " * event.span.depth
        agent = f"[{event.span.agent}]" if event.span.depth > 0 else ""

        match event.type:
            case EventType.AGENT_START:
                self._log(f"{indent}{agent} ▶ {event.data.get('task', '')[:50]}...")
            case EventType.AGENT_END:
                turns = event.data.get("turns", 0)
                self._log(f"{indent}{agent} ✓ Done ({turns} turns)")
            case EventType.LLM_START:
                if self.verbose:
                    self._log(f"{indent}{agent} 💭 Thinking...")
            case EventType.LLM_END:
                tokens = event.data.get("tokens", 0)
                tools = event.data.get("tool_calls", 0)
                self._log(f"{indent}{agent} 💬 ({tokens} tokens, {tools} tools)")
            case EventType.TOOL_START:
                self._log(f"{indent}{agent} 🔧 {event.data.get('name')}...")
            case EventType.TOOL_END:
                status = "✓" if event.data.get("success") else "✗"
                ms = event.data.get("duration_ms", 0)
                self._log(f"{indent}{agent} {status} {event.data.get('name')} ({ms}ms)")
            case EventType.DELEGATION_START:
                self._log(f"{indent}{agent} 📤 → {event.data.get('agent')}")
            case EventType.DELEGATION_END:
                self._log(f"{indent}{agent} 📥 ← done")
            case EventType.APPROVAL_REQUIRED:
                self._log(f"{indent}{agent} ⚠️  Approval: {event.data.get('tool')}")
            case EventType.TOOL_DENIED:
                self._log(f"{indent}{agent} 🚫 Denied: {event.data.get('tool')}")

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{ts} {msg}", file=self.output)
