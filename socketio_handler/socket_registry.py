from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from handler import BaseSocketHandler

    HandlerT = type["BaseSocketHandler"]
    HandlersT = dict[str, HandlerT]


class SocketHandlerRegistry:
    def __init__(self):
        self._handlers: "HandlersT" = {}  # noqa: UP037

    def register(self, handler_cls: "HandlerT", namespace: str = "/") -> None:
        self._handlers[namespace] = handler_cls

    def get_handler(self, namespace: str) -> Optional["HandlerT"]:
        return self._handlers.get(namespace)

    @property
    def handlers(self) -> "HandlersT":
        return self._handlers


handler_registry = SocketHandlerRegistry()


def register_handler(*, namespace: str = "/") -> Callable[["HandlerT"], "HandlerT"]:
    def decorator(cls: "HandlerT") -> "HandlerT":
        handler_registry.register(cls, namespace)
        return cls

    return decorator
