from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from socketio_handler.handler import BaseSocketHandler


class HandlerEntry(NamedTuple):
    namespace: str
    handler_cls: type["BaseSocketHandler"]
