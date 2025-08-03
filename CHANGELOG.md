# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
