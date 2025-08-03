import pytest
import socketio

from socketio_handler import BaseSocketHandler, SocketManager
from socketio_handler.socket_registry import get_handler_by_namespace, handler_registry, register_handler

pytestmark = [pytest.mark.asyncio]


async def test_socket_manager_mount_and_register(socket_manager):
    assert isinstance(socket_manager.sio, socketio.AsyncServer)
    assert not socket_manager._SocketManager__registered

    socket_manager.register_events()
    assert socket_manager._SocketManager__registered


async def test_duplicate_event_registration(socket_manager):
    socket_manager._SocketManager__registered = True
    socket_manager.register_events()


async def test_handler_registry():
    class DummyHandler(BaseSocketHandler):
        async def connect(self, sid, environ, auth=None):
            pass

        async def event_message(self, sid, data):
            pass

    handler_registry.register(DummyHandler, namespace="/dummy")
    handler = handler_registry.get_handler('/dummy')
    assert handler.namespace == '/dummy'
    assert handler.handler_cls is DummyHandler


async def test_register_handler_decorator():
    @register_handler(namespace="/test")
    class TestHandler(BaseSocketHandler):
        async def connect(self, sid, environ, auth=None):
            pass

        async def event_message(self, sid, data):
            pass

    handler = handler_registry.get_handler('/test')
    assert handler.namespace == '/test'
    assert handler.handler_cls is TestHandler


async def test_get_handler_by_namespace():

    @register_handler(namespace="/abc")
    class ABCHandler(BaseSocketHandler):
        async def connect(self, sid, environ, auth=None):
            pass

        async def event_message(self, sid, data):
            pass

    handler = get_handler_by_namespace("/abc")
    assert handler.namespace == '/abc'
    assert handler.handler_cls is ABCHandler


async def test_context_manager():
    async with SocketManager() as manager:
        assert isinstance(manager, SocketManager)
