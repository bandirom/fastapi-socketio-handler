from typing import TYPE_CHECKING, Callable, Optional

from socketio_handler.types import HandlerEntry

if TYPE_CHECKING:
    from handler import BaseSocketHandler


class SocketHandlerRegistry:
    def __init__(self):
        self._handlers: dict[str, HandlerEntry] = {}

    def register(self, handler_cls: type["BaseSocketHandler"], namespace: str = "/") -> None:
        self._handlers[namespace] = HandlerEntry(namespace=namespace, handler_cls=handler_cls)

    def get_handler(self, namespace: str) -> Optional[HandlerEntry]:
        return self._handlers.get(namespace)

    @property
    def handlers(self) -> dict[str, HandlerEntry]:
        return self._handlers


handler_registry = SocketHandlerRegistry()


def register_handler(*, namespace: str = "/") -> Callable[[type["BaseSocketHandler"]], type["BaseSocketHandler"]]:
    def decorator(cls: type["BaseSocketHandler"]) -> type["BaseSocketHandler"]:
        handler_registry.register(cls, namespace)
        return cls

    return decorator


def get_handler_by_namespace(namespace: str) -> Optional[HandlerEntry]:
    return handler_registry.get_handler(namespace)
