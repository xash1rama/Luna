from pydantic import BaseModel
from typing import List
from app.schemas.schemas_phone import Phone
from app.schemas.schemas_category import Category
from app.schemas.schemas_building import Building


class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    building_id: int
    category_ids: List[int]
    phone_numbers: List[str]

class Organization(OrganizationBase):
    id: int
    building: Building
    phones: List[Phone]
    categories: List[Category]

    class Config:
        from_attributes = True
