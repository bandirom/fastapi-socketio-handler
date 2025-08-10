import asyncio

import pytest

from socketio_handler import BaseSocketHandler, register_handler
from tests.conftest import FASTAPI_SERVER_HOST, FASTAPI_SERVER_PORT

pytestmark = [pytest.mark.asyncio]

SOCKETIO_NAMESPACE = "/test-1"


@register_handler(namespace=SOCKETIO_NAMESPACE)
class SocketTestHandler(BaseSocketHandler):
    async def on_connect(self, sid, environ, auth=None):
        await self.sio.emit("connect_ack", {"message": "connected"}, to=sid, namespace=self.namespace)

    async def on_echo(self, sid, data):
        await self.sio.emit("echo_response", {"echoed": data}, to=sid, namespace=self.namespace)


async def test_socketio_integration(sio_client_factory, run_server_in_thread):
    received = {}
    client = sio_client_factory()

    @client.on("connect_ack", namespace=SOCKETIO_NAMESPACE)
    async def on_connect_ack(data):
        received["connect"] = data

    @client.on("echo_response", namespace=SOCKETIO_NAMESPACE)
    async def on_echo_response(data):
        received["echo"] = data

    with run_server_in_thread():
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
