"""
Phase 1 app entrypoint.

Run it:
    uv run uvicorn phase1_routing.main:app --reload

The interesting bit is `include_router`: the app stays tiny while the actual
endpoints live in router.py. In a real project you'd have many routers
(items, users, auth, ...) each in their own file, all included here.
"""

from fastapi import FastAPI

from .router import router as items_router

app = FastAPI(
    title="FastAPI Learning — Phase 1",
    description="Routing, path/query/header params, request body, response models, status codes.",
    version="0.1.0",
)

# Plug the items router (prefix="/items") into the app.
app.include_router(items_router)


@app.get("/", tags=["root"])
def root():
    return {"message": "Phase 1 — see /docs", "try": "/items"}
