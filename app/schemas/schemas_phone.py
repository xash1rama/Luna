from pydantic import BaseModel


class PhoneBase(BaseModel):
    number: str

class Phone(PhoneBase):
    id: int
    class Config:
        from_attributes = True
