from typing import TYPE_CHECKING, Literal, NamedTuple, TypedDict

if TYPE_CHECKING:
    from socketio_handler.handler import BaseSocketHandler


class HandlerEntry(NamedTuple):
    namespace: str
    handler_cls: type["BaseSocketHandler"]


class InstrumentAuthDTO(TypedDict):
    username: str
    password: str


class InstrumentDTO(TypedDict, total=False):
    auth: InstrumentAuthDTO
    mode: Literal['development', 'production']
    read_only: bool
    server_id: str
    namespace: str
    server_stats_interval: int


class SocketManagerKwargs(TypedDict, total=False):
    logger: bool
    engineio_logger: bool
    transports: list[Literal['polling', 'websocket']]
