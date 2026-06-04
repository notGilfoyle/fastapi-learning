"""
Pydantic models used as REQUEST BODIES and RESPONSE MODELS in Phase 1.

We only scratch the surface of Pydantic here (just enough to do routing well).
Phase 2 is the deep dive. For now, the key idea:

    A Pydantic model = a typed description of a JSON object.
    FastAPI uses it to (a) validate incoming JSON and (b) shape outgoing JSON.
"""

from pydantic import BaseModel, Field


# ---- Input model: what the CLIENT sends us when creating an item ----
class ItemCreate(BaseModel):
    # `Field(...)` lets us add validation rules + docs.
    # The "..." (Ellipsis) means "required, no default".
    name: str = Field(..., min_length=1, max_length=50, description="Item name")
    price: float = Field(..., gt=0, description="Price in USD, must be > 0")
    # Optional field with a default. `str | None` = "string or null".
    description: str | None = Field(default=None, max_length=300)
    in_stock: bool = True


# ---- Output model: what WE send back ----
# Notice it has an `id` (assigned by the server) that the input model didn't.
# Splitting "Create" (input) from "Read" (output) models is a common, healthy
# pattern: clients shouldn't send an id, but we want to return one.
class ItemRead(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    in_stock: bool
