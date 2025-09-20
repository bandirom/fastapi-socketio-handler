import logging
from typing import TYPE_CHECKING, Optional, Unpack, cast

from socketio import ASGIApp, AsyncRedisManager, AsyncServer

from .socket_registry import handler_registry
from .types import InstrumentDTO, SocketManagerKwargs

if TYPE_CHECKING:
    from fastapi import FastAPI
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from .handler import BaseSocketHandler


logger = logging.getLogger(__name__)


class SocketManager:

    def __init__(
        self,
        *,
        socketio_path: str = "socket.io",
        cors_allowed_origins: list[str] = None,
        async_mode: str = "asgi",
        async_session: Optional["async_sessionmaker"] = None,
        redis_url: str = None,
        instrument: Optional[InstrumentDTO] = None,
        **kwargs: Unpack[SocketManagerKwargs],
    ):
        if cors_allowed_origins is None:
            cors_allowed_origins = []
        if redis_url:
            logger.info("[sio] Using Redis manager")
            cast(dict[str, AsyncRedisManager], kwargs)["client_manager"] = AsyncRedisManager(redis_url)

        self._sio = AsyncServer(async_mode=async_mode, cors_allowed_origins=cors_allowed_origins, **kwargs)
        self._app = ASGIApp(socketio_server=self._sio, socketio_path=socketio_path)
        self.session_factory = async_session

        if instrument:
            self._sio.instrument(**instrument)

        self.__registered = False
        logger.debug("[sio] SocketManager initialized")

    def mount_to_app(self, fastapi_app: "FastAPI", mount_location: str = "/socket.io/") -> None:
        """Set FastAPI application instance."""
        fastapi_app.mount(mount_location, self._app)
        fastapi_app.sio = self._sio
        fastapi_app.state.socket_manager = self
        logger.info(f"[sio] Mounted at {mount_location}")

    @property
    def sio(self) -> AsyncServer:
        """Returns the SocketIO server instance."""
        return self._sio

    def register_handlers(self, **kwargs):
        if self.__registered:
            logger.warning("[sio] Events already registered. Skipping.")
            return
        logger.info("[sio] Registering event handlers")
        for namespace, handler_cls in handler_registry.handlers.items():
            logger.debug(f"[sio] Registering handler: {handler_cls.__name__} for namespace: {namespace}")
            handler = handler_cls(
                sio=self._sio,
                session_factory=self.session_factory,
                namespace=namespace,
                **kwargs,
            )
            self._sio.register_namespace(handler)
        self.__registered = True

    def get_namespace_handler(self, namespace: str) -> "BaseSocketHandler":
        return self._sio.namespace_handlers[namespace]

    async def __aenter__(self):
        logger.info("[sio] entering async context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info("[sio] exiting async context")
        await self._sio.shutdown()
