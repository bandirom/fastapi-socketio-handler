import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from socketio import AsyncServer
    from sqlalchemy.ext.asyncio import async_sessionmaker


logger = logging.getLogger(__name__)


class BaseSocketHandler(ABC):

    def __init__(
        self,
        sio: "AsyncServer",
        session_factory: "async_sessionmaker",
        namespace: str = "/",
    ):
        self.sio = sio
        self.namespace = namespace
        self.session_factory = session_factory
        self.register_default_events()

    def register_default_events(self):
        self.sio.on("connect", self.connect, namespace=self.namespace)
        self.sio.on("disconnect", self.disconnect, namespace=self.namespace)

    def register_events(self):  # noqa: B027
        """
        Register socket events for the handler.
        This method should be overridden by subclasses to register specific events.
        """
        pass

    @abstractmethod
    async def connect(self, sid: str, environ: dict, auth: Optional[dict] = None):
        """
        Handle the connection event.
        This method should be overridden by subclasses to handle connection logic.
        """
        pass

    async def disconnect(self, sid: str):
        logger.debug(f"Client disconnected: {sid}")
