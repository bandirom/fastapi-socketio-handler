from collections.abc import AsyncGenerator
from typing import Callable

import pytest
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient as AsyncHttpClient
from socketio import AsyncClient

from socketio_handler import SocketManager

FASTAPI_SERVER_HOST = "localhost"
FASTAPI_SERVER_PORT = 8000


@pytest.fixture()
def socket_manager():
    return SocketManager(async_session=None)


@pytest.fixture(scope="session")
def fastapi_app() -> FastAPI:
    app = FastAPI()
    return app


@pytest.fixture(scope="function")
async def http_client(fastapi_app) -> AsyncGenerator[AsyncHttpClient, None]:
    async with AsyncHttpClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
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
