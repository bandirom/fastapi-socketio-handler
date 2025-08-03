# Contributing to fastapi-socketio-handler

Welcome, and thanks for taking the time to contribute! 🎉

This guide will help you set up your environment and follow our contribution standards.

---

## 🛠️ Setup

```shell
git clone https://github.com/bandirom/fastapi-socketio-handler.git
cd fastapi-socketio-handler

poetry install --with dev
poetry shell
```

## 📐 Code Style

We use:
* `black` for formatting
* `ruff` for linting

`line-length = 120` and `skip-string-normalization = true`

To check before pushing:

```shell
ruff check . --fix
black .
```

## 🧪 Testing
Tests are written with pytest:

```shell
pytest
```

## 📦 Adding a Feature or Fix

1. Fork the repo
2. Create a new branch: git checkout -b feat/your-feature
3. Add/commit your code and tests
4. Run pytest, ruff, and black
5. Submit a Pull Request with a clear description


## 📜 Versioning
We follow SemVer. Any public API changes should bump the version accordingly


### 🙏 Thanks!
You're awesome for considering contributing
