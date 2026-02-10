import sys
import json
import asyncio
from uuid import uuid4
from typing import Any

from ..models import Event, EventType, Span


class StdioTransport:
    JSONRPC_SERVER_ERROR = -32000
    JSONRPC_METHOD_NOT_FOUND = -32601

    def __init__(self):
        self._pending_requests: dict[str, asyncio.Future] = {}
        self._output_lock = asyncio.Lock()
        self._loop: asyncio.AbstractEventLoop | None = None

    def handle(self, event: Event) -> None:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._write_event(event))
        except RuntimeError:
            pass

    async def _write_event(self, event: Event):
        async with self._output_lock:
            sys.stdout.write(json.dumps(event.to_dict()) + "\n")
            sys.stdout.flush()

    async def human_input_fn(self, prompt: str, span: Span | None = None) -> str:
        req_id = uuid4().hex

        await self._write_event(
            Event(
                type=EventType.HUMAN_INPUT_WAITING,
                span=span or Span(),
                data={"prompt": prompt, "request_id": req_id},
            )
        )

        future = asyncio.get_event_loop().create_future()
        self._pending_requests[req_id] = future

        try:
            response = await asyncio.wait_for(future, timeout=300)
            return response.get("response", "")
        finally:
            self._pending_requests.pop(req_id, None)

    async def approval_fn(
        self, tool: str, args: dict, span: Span | None = None
    ) -> bool:
        req_id = uuid4().hex

        await self._write_event(
            Event(
                type=EventType.APPROVAL_REQUIRED,
                span=span or Span(),
                data={"tool": tool, "args": args, "request_id": req_id},
            )
        )

        future = asyncio.get_event_loop().create_future()
        self._pending_requests[req_id] = future

        try:
            response = await asyncio.wait_for(future, timeout=300)
            return response.get("approved", False)
        finally:
            self._pending_requests.pop(req_id, None)

    def handle_response(self, request_id: str, data: dict):
        if request_id in self._pending_requests:
            self._pending_requests[request_id].set_result(data)

    async def read_stdin(self):
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while True:
            line = await reader.readline()
            if not line:
                break

            try:
                message = json.loads(line.decode())
                yield message
            except json.JSONDecodeError:
                continue

    async def send_response(
        self, message_id: Any, result: Any = None, error: Any = None
    ):
        response = {"jsonrpc": "2.0", "id": message_id}
        if error:
            response["error"] = error
        else:
            response["result"] = result

        async with self._output_lock:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

    async def send_error(self, message_id: Any, code: int, message: str):
        await self.send_response(message_id, error={"code": code, "message": message})
