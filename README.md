# FastAPI Learning 🚀

A hands-on, phase-by-phase journey through FastAPI's core concepts.
Each phase has runnable code (heavily commented) and a `NOTES.md` that doubles as a revision sheet.

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) to manage Python and dependencies.

```bash
# Install deps + create the virtual env (reads pyproject.toml / uv.lock)
uv sync

# Run any phase's app, e.g. phase 0:
uv run uvicorn phase0_setup.main:app --reload
```

Then open:
- http://127.0.0.1:8000 — the app
- http://127.0.0.1:8000/docs — interactive Swagger UI (auto-generated)
- http://127.0.0.1:8000/redoc — alternative ReDoc docs

## Phases

| Phase | Topic |
|-------|-------|
| 0 | Setup — project, FastAPI, hello world, the docs UI |
| 1 | Routing & path params |
| 2 | Pydantic v2 deep dive |
| 3 | Dependency injection |
| 4 | Middleware & CORS |
| 5 | Error handling |
| 6 | Background tasks & lifespan |
| 7 | Async & performance |
