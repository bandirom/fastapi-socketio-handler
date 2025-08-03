import asyncio
import threading
import time

import pytest

from socketio_handler import BaseSocketHandler, register_handler
from tests.conftest import FASTAPI_SERVER_HOST, FASTAPI_SERVER_PORT

pytestmark = [pytest.mark.asyncio]

SOCKETIO_NAMESPACE = "/test-1"


@register_handler(namespace=SOCKETIO_NAMESPACE)
class SocketTestHandler(BaseSocketHandler):
    def register_events(self):
        self.sio.on("echo", self.event_echo, namespace=self.namespace)

    async def connect(self, sid, environ, auth=None):
        await self.sio.emit("connect_ack", {"message": "connected"}, to=sid, namespace=self.namespace)

    async def event_echo(self, sid, data):
        await self.sio.emit("echo_response", {"echoed": data}, to=sid, namespace=self.namespace)


@pytest.fixture
async def mounted_socket_manager(socket_manager, fastapi_app):
    socket_manager.mount_to_app(fastapi_app)
    socket_manager.register_events()
    return socket_manager


@pytest.fixture
def run_server_in_thread(fastapi_app, mounted_socket_manager):
    from uvicorn import Config, Server

    config = Config(fastapi_app, host=FASTAPI_SERVER_HOST, port=FASTAPI_SERVER_PORT, log_level="error")
    server = Server(config)

    thread = threading.Thread(target=server.run)
    thread.start()
    time.sleep(0.5)
    yield

    server.should_exit = True
    thread.join()


async def test_socketio_integration(sio_client_factory, run_server_in_thread):
    received = {}
    client = sio_client_factory()

    @client.on("connect_ack", namespace=SOCKETIO_NAMESPACE)
    async def on_connect_ack(data):
        received["connect"] = data

    @client.on("echo_response", namespace=SOCKETIO_NAMESPACE)
    async def on_echo_response(data):
        received["echo"] = data

    await client.connect(
        f"http://{FASTAPI_SERVER_HOST}:{FASTAPI_SERVER_PORT}",
        socketio_path="socket.io",
        namespaces=[SOCKETIO_NAMESPACE],
    )

    await client.emit("echo", {"msg": "hello"}, namespace=SOCKETIO_NAMESPACE)

    for _ in range(10):
        if "connect" in received and "echo" in received:
            break
        await asyncio.sleep(0.1)

    assert received["connect"] == {"message": "connected"}
    assert received["echo"] == {"echoed": {"msg": "hello"}}
