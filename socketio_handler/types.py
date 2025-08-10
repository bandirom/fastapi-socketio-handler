from typing import TYPE_CHECKING, Literal, NamedTuple, Optional, TypedDict

if TYPE_CHECKING:
    from socketio_handler.handler import BaseSocketHandler


class HandlerEntry(NamedTuple):
    namespace: str
    handler_cls: type["BaseSocketHandler"]


class InstrumentKwargs(TypedDict, total=False):
    auth: dict[str, str]
    mode: Literal['development', 'production']
    read_only: bool
    server_id: str
    namespace: str
    server_stats_interval: int


class SocketManagerKwargs(TypedDict, total=False):
    instrument: Optional[InstrumentKwargs]
