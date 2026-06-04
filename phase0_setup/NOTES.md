# Phase 0 — Setup & Hello World 📝

## What is FastAPI, really?

FastAPI is a Python web framework for building **APIs** (services that speak HTTP/JSON,
not HTML pages). Its three selling points:

1. **Speed of writing** — you describe your data with normal Python type hints,
   and FastAPI does validation, parsing, and documentation for you.
2. **Speed of running** — it's built on **Starlette** (async web toolkit) and
   **Pydantic** (data validation). It's one of the fastest Python frameworks.
3. **Free interactive docs** — every endpoint shows up at `/docs` automatically.

Mental model of the stack:

```
   Your code (routes, models)
        │  uses
   FastAPI            ← routing, validation, docs, dependency injection
    ├── Starlette     ← the actual async web server plumbing (ASGI)
    └── Pydantic      ← data models & validation (Phase 2 goes deep here)
        │  served by
   Uvicorn            ← the ASGI server that actually listens on a port
```

## Key vocabulary

| Term | Meaning |
|------|---------|
| **ASGI** | Async Server Gateway Interface — the modern Python web standard FastAPI speaks. (WSGI was the old, sync-only one used by Flask/Django.) |
| **Uvicorn** | The program that runs your ASGI app and listens for HTTP requests. |
| **Path operation** | A route = an HTTP method (GET/POST/...) + a path (`/users`) + the function that handles it. |
| **Path operation function** | The Python function decorated with `@app.get(...)` etc. |

## The one command to remember

```bash
uv run uvicorn phase0_setup.main:app --reload
```

- `uv run` → run inside the project's virtual env (no manual `activate` needed)
- `uvicorn` → the server
- `phase0_setup.main:app` → `module:variable` pointing at the FastAPI instance
- `--reload` → auto-restart on file save (dev only)

## Why the docs UI is a big deal

Open http://127.0.0.1:8000/docs. That **Swagger UI** is generated from your code —
no extra work. You can click "Try it out" and call your API from the browser.
It's powered by the **OpenAPI** schema FastAPI builds; you can see the raw JSON
at `/openapi.json`. As we add typed params and models in later phases, watch this
page get richer automatically.

## Returning data

Returning a `dict` is the quick path — FastAPI converts it to JSON. In Phase 1+
we'll return **Pydantic models** instead, which gives us validation + a documented
response shape.

---

### ✅ Phase 0 checklist
- [x] `uv` project created (Python 3.12)
- [x] `fastapi` + `uvicorn` installed
- [x] First two routes (`/` and `/health`)
- [x] Confirmed `/docs` works
