# Fastapi-socketio-handler

**FastAPI + Socket.IO integration made modular, extensible and simple.**

A clean event-based wrapper that helps you organize your Socket.IO server logic using decorators, handlers, and namespaces.

---

## 🔧 Features

- 📡 Socket.IO server for FastAPI apps
- 🧩 Handler registration via decorators
- 📁 Namespace-based routing
- 🔁 Redis pub/sub support (scaling)
- 💡 Typed, extensible, and testable architecture
- 🧪 Ready for pytest & async testing

---

## 📦 Installation

```shell
pip install fastapi-socketio-handler
```


## 🚀 Quick Start


### 1. Define a handler

```python
# app/chat_handler.py

from socketio_handler import BaseSocketHandler, register_handler


@register_handler(namespace="/chat")
class ChatSocketHandlers(BaseSocketHandler):

    async def on_connect(self, sid: str, environ: dict, auth: dict = None):
        if not auth or "token" not in auth:
            return False  # Reject connection
        return True

    async def on_typing(self, sid: str, data: dict, *args):
        print(f'Typing event from {sid}: {data}', args)

    async def on_stop_typing(self, sid: str, data: dict, *args):
        print(f'StopTyping event from {sid}: {data}', args)
```


### 2. Use with lifespan (recommended)

```python
# core/db.py
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url="database_uri", echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)
```

```python
# core/lifespan.py
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from socketio_handler import SocketManager

from .db import async_session

import app.chat_handler  # 👈 force-import handlers to trigger decorator registration

if TYPE_CHECKING:
    from fastapi import FastAPI
    
@asynccontextmanager
async def lifespan(app: "FastAPI"):
    """
    Lifespan context manager for FastAPI application.
    Useful for initializing and cleaning up resources.
    """
    async with (
        SocketManager(
            redis_url="redis://localhost:6379",
            async_session=async_session,
        ) as socket_manager,
    ):
        socket_manager.mount_to_app(app)
        socket_manager.register_handlers()
        app.state.socket_manager = socket_manager
        yield
```

```python
# main.py
from fastapi import FastAPI
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
```


### 3. Connect from frontend
```javascript
const socket = io('http://localhost:8000/chat', {
  auth: {
    token: 'your-auth-token'
  }
});

socket.emit("typing", { chatId: "..." });
```


## 🧪 Testing

This package includes pytest-based test utilities.  
You can run the tests with:

* Install dependencies for testing
```shell
poetry install --with dev
```

* Run tests
```shell
pytest
```
