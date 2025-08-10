import logging
from typing import TYPE_CHECKING

from socketio import AsyncNamespace

if TYPE_CHECKING:
    from socketio import AsyncServer
    from sqlalchemy.ext.asyncio import async_sessionmaker


logger = logging.getLogger(__name__)


class BaseSocketHandler(AsyncNamespace):

    def __init__(
        self,
        sio: "AsyncServer",
        session_factory: "async_sessionmaker",
        namespace: str = "/",
    ):
        self.sio = sio
        self.session_factory = session_factory
        super().__init__(namespace)
