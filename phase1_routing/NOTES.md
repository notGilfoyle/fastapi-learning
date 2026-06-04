# Phase 1 — Routing & Parameters 📝

The whole phase in one sentence: **a type hint on a function parameter tells
FastAPI where to read the value from AND how to validate it.**

## The 5 ways data enters an endpoint

| Source | How FastAPI decides | Example |
|--------|---------------------|---------|
| **Path param** | name appears inside `{...}` in the path | `/items/{item_id}` |
| **Query param** | a simple-typed arg NOT in the path | `/items?limit=10` |
| **Header param** | declared with `Header(...)` | `User-Agent` |
| **Request body** | arg typed as a **Pydantic model** | `payload: ItemCreate` |
| (Cookie param) | declared with `Cookie(...)` | not used here |

The rule FastAPI follows for each function argument:
1. Is the name in the path? → **path param**
2. Is it a Pydantic model? → **request body**
3. Is it declared `Header`/`Cookie`/`Query`? → that source
4. Otherwise, simple type (int/str/bool/...) → **query param**

## Path parameters

```python
@router.get("/{item_id}")
def get_item(item_id: int):   # int hint => /items/abc auto-returns 422
    ...
```
The `int` hint does conversion + validation for free. No hint = it's just a string.

## Query parameters

A simple-typed arg with a default becomes an optional query param:
```python
def list_items(skip: int = 0, limit: int = Query(10, ge=1, le=100)):
```
- No default → **required** query param.
- `Query(...)` is the explicit form; use it to add `ge`/`le`/`min_length`/docs.
- `q: str | None = None` → optional, may be absent.

## Header parameters

```python
def inspect_headers(user_agent: str | None = Header(default=None)):
```
FastAPI maps `user_agent` ⇄ the `User-Agent` header (underscore → hyphen).
Use `Header(convert_underscores=False)` for verbatim names.

## Request body (Pydantic model)

Type a parameter as a Pydantic model and FastAPI reads + validates the JSON body:
```python
def create_item(payload: ItemCreate):
    record = payload.model_dump()   # Pydantic v2: model -> dict
```
Invalid body (e.g. `price: -1` when rule is `gt=0`) → automatic **422** with a
precise error pointing at the bad field.

## Response models

```python
@router.post("", response_model=ItemRead, status_code=201)
```
- `response_model=ItemRead` → output is validated and **filtered** to that shape.
  Great for hiding internal fields (e.g. password hashes) — anything not in the
  model is stripped from the response.
- Common pattern: separate **`Create`** (input) and **`Read`** (output) models.

## Status codes

Return the right HTTP code:
- `200` OK (default for GET)
- `201` Created (after a successful POST) → `status_code=status.HTTP_201_CREATED`
- `404` Not Found → `raise HTTPException(status_code=404, detail=...)`
- `422` Unprocessable Entity → FastAPI raises this automatically on bad input

Import readable constants from `fastapi.status` instead of magic numbers.

## APIRouter — organizing a real app

```python
router = APIRouter(prefix="/items", tags=["items"])
...
app.include_router(router)
```
- `prefix` is prepended to every route in the file → `@router.get("")` = `GET /items`.
- `tags` group endpoints in `/docs`.
- One router per resource keeps `main.py` tiny and the project navigable.

---

### ✅ Verified behaviour (all tested)
| Request | Result |
|---------|--------|
| `GET /items/1` | the notebook item |
| `GET /items/abc` | **422** (int validation) |
| `GET /items/999` | **404** with detail |
| `GET /items?limit=1` | one item |
| `GET /items?q=pen` | the Pen, filtered |
| `GET /items?limit=999` | **422** (le=100) |
| `GET /items/inspect-headers` (with `X-Request-Id`) | echoes headers |
| `POST /items` valid body | **201** + ItemRead |
| `POST /items` `price=-1` | **422** (gt=0) |
