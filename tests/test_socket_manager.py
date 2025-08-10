import pytest
import socketio

from socketio_handler import BaseSocketHandler, SocketManager
from socketio_handler.socket_registry import handler_registry, register_handler

pytestmark = [pytest.mark.asyncio]


async def test_socket_manager_mount_and_register(socket_manager):
    assert isinstance(socket_manager.sio, socketio.AsyncServer)
    assert not socket_manager._SocketManager__registered

    socket_manager.register_handlers()
    assert socket_manager._SocketManager__registered


async def test_duplicate_event_registration(socket_manager):
    socket_manager._SocketManager__registered = True
    socket_manager.register_handlers()


async def test_handler_registry():
    class DummyHandler(BaseSocketHandler):
        async def on_connect(self, sid, environ, auth=None):
            pass

        async def on_message(self, sid, data):
            pass

    handler_registry.register(DummyHandler, namespace="/dummy")
    handler = handler_registry.get_handler('/dummy')
    assert handler is DummyHandler


async def test_register_handler_decorator():
    @register_handler(namespace="/test")
    class TestHandler(BaseSocketHandler):
        async def on_connect(self, sid, environ, auth=None):
            pass

        async def on_message(self, sid, data):
            pass

    handler = handler_registry.get_handler('/test')
    assert handler is TestHandler


async def test_context_manager():
    async with SocketManager() as manager:
        assert isinstance(manager, SocketManager)
