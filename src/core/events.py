from .models import Event, EventType, EventData, Span, EventHandler


class Emitter:
    def __init__(self, handler: EventHandler | None, span: Span):
        self._handler = handler
        self.span = span

    def emit(self, type: EventType, data: EventData | None = None) -> None:
        if self._handler:
            self._handler(Event(type, self.span, data or {}))

    def child(self, agent: str) -> "Emitter":
        return Emitter(self._handler, self.span.child(agent))

    @classmethod
    def null(cls) -> "Emitter":
        return cls(None, Span())


def combine(*handlers: EventHandler) -> EventHandler:
    def combined(event: Event):
        for h in handlers:
            try:
                h(event)
            except Exception:
                pass

    return combined
