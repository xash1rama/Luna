from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True
