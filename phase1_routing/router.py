"""
Phase 1 — Routing & Parameters
==============================

This file defines an APIRouter that demonstrates the five ways data gets INTO an
endpoint, plus how we shape what comes OUT.

    1. Path parameters    -> part of the URL path     /items/{item_id}
    2. Query parameters   -> after the ? in the URL    /items?skip=0&limit=10
    3. Header parameters  -> HTTP request headers      User-Agent: ...
    4. Request body       -> JSON payload (POST/PUT)   {"name": "Pen", ...}
    5. Response model     -> the declared output shape (response_model=...)

Plus status codes (201 Created, 404 Not Found, ...).
"""

from fastapi import APIRouter, Header, HTTPException, Query, status

from .schemas import ItemCreate, ItemRead

# ----------------------------------------------------------------------------
# APIRouter: a "mini-app" you can define in its own file and plug into the main
# app with `app.include_router(...)`. This is how you keep large projects tidy
# (one router per resource: items, users, orders, ...).
#
#   prefix="/items"  -> every path below is automatically prefixed, so
#                       @router.get("") is really GET /items
#   tags=["items"]   -> groups these endpoints together in the /docs UI
# ----------------------------------------------------------------------------
router = APIRouter(prefix="/items", tags=["items"])


# A fake in-memory "database" so we have something to read/write.
# (Real persistence comes much later; this keeps Phase 1 focused on routing.)
_FAKE_DB: dict[int, dict] = {
    1: {"id": 1, "name": "Notebook", "price": 4.5, "description": "A5, dotted", "in_stock": True},
    2: {"id": 2, "name": "Pen", "price": 1.2, "description": None, "in_stock": False},
}


# ============================================================================
# 1 + 2) QUERY PARAMETERS (and the LIST endpoint)
# ============================================================================
# Function parameters that are NOT in the path and are NOT a Pydantic model
# become QUERY parameters automatically.
#
#   GET /items?skip=0&limit=10&q=pen
#
# Defaults make them optional. Type hints (int, str|None) drive validation:
# /items?limit=abc -> automatic 422 error, you write zero validation code.
@router.get("", response_model=list[ItemRead])
def list_items(
    skip: int = 0,
    # Query(...) is the explicit form — use it when you want validation/docs.
    # le=100 means "less than or equal to 100".
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
    q: str | None = Query(default=None, description="Optional name search"),
):
    items = list(_FAKE_DB.values())
    if q:
        items = [it for it in items if q.lower() in it["name"].lower()]
    return items[skip : skip + limit]


# ============================================================================
# 3) HEADER PARAMETERS
# ============================================================================
# `Header(...)` pulls a value from the request headers. FastAPI auto-converts
# the Python name `user_agent` to the header name `User-Agent` (underscores ->
# hyphens). Set convert_underscores=False to read exotic header names verbatim.
@router.get("/inspect-headers")
def inspect_headers(
    user_agent: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None, description="Custom trace id"),
):
    return {"user_agent": user_agent, "x_request_id": x_request_id}


# ============================================================================
# 1) PATH PARAMETERS (and a single-item READ)
# ============================================================================
# {item_id} in the path maps to the `item_id` function arg. The `int` type hint
# means FastAPI validates & converts it: /items/abc -> 422 automatically.
#
# We raise HTTPException(404) when the item is missing — more on errors in Ph 5.
@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int):
    item = _FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


# ============================================================================
# 4 + 5) REQUEST BODY + RESPONSE MODEL + STATUS CODE
# ============================================================================
# Declaring a parameter typed as a Pydantic model => FastAPI reads it from the
# JSON request BODY, validates it, and hands you a typed object.
#
#   response_model=ItemRead   -> output is validated & filtered to this shape
#                                (any extra fields would be stripped) and the
#                                docs show the exact response schema.
#   status_code=201           -> correct code for "resource created".
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    new_id = max(_FAKE_DB) + 1 if _FAKE_DB else 1
    # model_dump() turns the Pydantic object into a plain dict (Pydantic v2 API).
    record = {"id": new_id, **payload.model_dump()}
    _FAKE_DB[new_id] = record
    return record
