# fastapi-socketio-handler

**FastAPI + Socket.IO integration made modular, extensible and simple.**

A clean event-based wrapper that helps you organize your Socket.IO server logic using decorators, handlers, and namespaces — powered by `python-socketio`, `FastAPI`, and `asyncio`.

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

from fastapi_socketio_handler import BaseSocketHandler, register_handler


@register_handler(namespace="/chat")
class ChatSocketHandlers(BaseSocketHandler):

    def register_events(self):
        self.sio.on("typing", self.event_typing, namespace=self.namespace)
        self.sio.on("stop_typing", self.event_stop_typing, namespace=self.namespace)

    async def connect(self, sid: str, environ: dict, auth: dict = None):
        if not auth or "token" not in auth:
            return False  # Reject connection
        return True

    async def event_typing(self, sid: str, data: dict):
        print(f"Typing: {data}")

    async def event_stop_typing(self, sid: str, data: dict):
        print(f"Stopped typing: {data}")
```


### 2. Use with lifespan (recommended)
```python
# lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_socketio_handler import get_socket_manager

import app.chat_handler  # 👈 force-import handlers to trigger decorator registration

@asynccontextmanager
async def lifespan(app: FastAPI):
    socket_manager = get_socket_manager(
        redis_url="redis://localhost:6379",           # Optional Redis
        async_session=your_async_session_factory,     # Optional DB session factory
    )
    socket_manager.mount_to_app(app)
    socket_manager.register_events()

    async with socket_manager:
        yield
```

### 3. Connect from frontend
```js
const socket = io('http://localhost:8000/chat', {
  auth: {
    token: 'your-auth-token'
  }
});

socket.emit("typing", { chatId: "..." });
```
