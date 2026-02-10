"""Session transport - writes events to JSONL file."""

import json
from datetime import datetime
from pathlib import Path

from ..models import Event, EventType, Span


class Session:
    """
    Writes events to JSONL file.
    
    That's it. Just a handler that writes.
    """
    
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def handle(self, event: Event) -> None:
        """Write event to file. This IS the event handler."""
        with open(self.path, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")
    
    def events(self) -> list[Event]:
        """Read all events back."""
        if not self.path.exists():
            return []
        
        events = []
        with open(self.path) as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    events.append(Event(
                        type=EventType(data["type"]),
                        span=Span(**data["span"]),
                        data=data["data"],
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                    ))
        return events
    
    @classmethod
    def new(cls, dir: Path = Path(".sessions")) -> "Session":
        """Create new session with timestamp-based filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return cls(dir / f"{timestamp}.jsonl")
