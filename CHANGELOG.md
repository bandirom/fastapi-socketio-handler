# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


---

## [0.2.0] - 2025-08-10

### Changed
- **BaseSocketHandler** now inherits from [`socketio.AsyncNamespace`](https://python-socketio.readthedocs.io/en/latest/api.html#socketio.AsyncNamespace) instead of a custom base class.
  - Simplifies integration with the official Socket.IO API.
  - Native support for standard events (`on_connect`, `on_disconnect`, etc.) without extra boilerplate.
- **Renamed**: `register_events()` → `register_handlers()` for consistency with FastAPI naming conventions.
- Updated internal logic in `SocketManager.register_handlers()` for compatibility with the new `SocketHandler` type.

### Added
- Graceful shutdown support: `await self._sio.shutdown()` is now called during `SocketManager` cleanup.

### Fixed
- Improved compatibility with asynchronous event handlers.

### Migration Notes
- If your handlers had methods named after events (`on_*`), they will now be called automatically without explicit registration.
- Update your code to call `register_handlers()` instead of `register_events()`.

---

## [v0.1.1] - 2025-08-03

### Added
- New tests for handler registration and manager lifecycle
- Improved `README.md` with usage examples, lifespan setup, and frontend integration
- Added contributing guidelines in `CONTRIBUTING.md`

### Changed
- Moved `SQLAlchemy` from runtime to dev dependencies (used only for type hints)

---

## [0.1.0] - 2025-08-03

### Added
- `SocketManager`: a core class for integrating Socket.IO with FastAPI.
- `BaseSocketHandler`: an abstract base class for socket event handlers with `register_events()` method.
- `register_handler()`: a decorator for registering socket handlers with a specific namespace.
- `handler_registry`: registry to keep track of all socket handlers.
- Redis support via `AsyncRedisManager` using the `redis_url` parameter.
- `mount_to_app()` method for attaching the Socket.IO server to a FastAPI app.
- Full unit test and integration test coverage with `pytest`.
- GitHub Actions CI with jobs for:
  - `ruff` (linter and formatter)
  - `black` (formatter)
  - `pytest` (tests for Python 3.9–3.13)

---
