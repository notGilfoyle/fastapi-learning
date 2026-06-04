"""
Phase 0 — Setup & "Hello, FastAPI"
==================================

Goal: prove the toolchain works and meet the three objects you'll see in EVERY
FastAPI app: the `FastAPI` instance, a "path operation" (route), and the
auto-generated docs.

Run it:
    uv run uvicorn phase0_setup.main:app --reload

The string "phase0_setup.main:app" reads as:  <module path>:<variable name>
i.e. "import the `app` object from phase0_setup/main.py".  --reload restarts the
server whenever you save a file (great for learning, never use in production).
"""

from fastapi import FastAPI

# 1) The application object.
#    `app` is the central registry: every route, middleware, and event handler
#    attaches to it. The title/description/version below show up in the docs UI.
app = FastAPI(
    title="FastAPI Learning — Phase 0",
    description="The smallest possible FastAPI app, with the docs turned on.",
    version="0.1.0",
)


# 2) A "path operation".
#    @app.get("/") = "when an HTTP GET arrives at path '/', call this function".
#    The function is called a *path operation function*. Its return value is
#    automatically converted to JSON for the response.
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! 🚀", "next": "visit /docs"}


# 3) A second route so you can see more than one entry in the docs.
#    Returning a dict is the simplest case; FastAPI serializes it to JSON and
#    sets Content-Type: application/json for you.
@app.get("/health")
def health_check():
    return {"status": "ok"}
