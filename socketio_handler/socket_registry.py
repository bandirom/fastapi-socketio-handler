from typing import TYPE_CHECKING, Callable, Type

if TYPE_CHECKING:
    from handler import BaseSocketHandler


class SocketHandlerRegistry:
    def __init__(self):
        self._handlers: list[tuple[str, Type["BaseSocketHandler"]]] = []

    def register(self, handler_cls: Type["BaseSocketHandler"], namespace: str = "/") -> None:
        self._handlers.append((namespace, handler_cls))

    def get_handlers(self) -> list[tuple[str, Type["BaseSocketHandler"]]]:
        return self._handlers


handler_registry = SocketHandlerRegistry()


def register_handler(*, namespace: str = "/") -> Callable[[Type["BaseSocketHandler"]], Type["BaseSocketHandler"]]:
    def decorator(cls: Type["BaseSocketHandler"]) -> Type["BaseSocketHandler"]:
        handler_registry.register(cls, namespace)
        return cls

    return decorator


def get_handler_by_namespace(namespace: str) -> Type["BaseSocketHandler"] | None:
    for ns, handler_cls in handler_registry.get_handlers():
        if ns == namespace:
            return handler_cls
    return None
