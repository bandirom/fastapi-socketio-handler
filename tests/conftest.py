import time
from collections.abc import AsyncGenerator
from contextlib import contextmanager
from threading import Thread
from typing import Callable, NamedTuple, Unpack

import pytest
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient as AsyncHttpClient
from socketio import AsyncClient
from uvicorn import Config, Server

from socketio_handler import SocketManager
from socketio_handler.types import SocketManagerKwargs

FASTAPI_SERVER_HOST = "localhost"
FASTAPI_SERVER_PORT = 8000


@pytest.fixture()
def socket_manager_factory():
    def factory(**kwargs: Unpack[SocketManagerKwargs]) -> SocketManager:
        return SocketManager(**kwargs)

    return factory


@pytest.fixture()
def socket_manager(socket_manager_factory) -> SocketManager:
    return socket_manager_factory()


@pytest.fixture(scope="session")
def fastapi_app() -> FastAPI:
    app = FastAPI()
    return app


@pytest.fixture()
async def http_client(fastapi_app) -> AsyncGenerator[AsyncHttpClient, None]:
    async with AsyncHttpClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture()
async def sio_client_factory() -> AsyncGenerator[Callable[[], AsyncClient], None]:
    clients: list[AsyncClient] = []

    def factory() -> AsyncClient:
        client = AsyncClient()
        clients.append(client)
        return client

    yield factory

    for client in clients:
        if client.connected:
            await client.disconnect()


@pytest.fixture()
async def mounted_socket_manager(socket_manager_factory, fastapi_app):
    def factory(**kwargs: Unpack[SocketManagerKwargs]) -> SocketManager:
        sm = socket_manager_factory(**kwargs)
        sm.mount_to_app(fastapi_app)
        sm.register_handlers()
        return sm

    return factory


@pytest.fixture
def run_server_in_thread(fastapi_app, mounted_socket_manager):
    @contextmanager
    def factory(**socket_manager_kwargs):
        sm = mounted_socket_manager(**socket_manager_kwargs)

        config = Config(fastapi_app, host=FASTAPI_SERVER_HOST, port=FASTAPI_SERVER_PORT, log_level="error")
        server = Server(config)

        thread = Thread(target=server.run)
        thread.start()
        time.sleep(0.5)

        try:
            yield sm
        finally:
            server.should_exit = True
            thread.join()

    return factory
