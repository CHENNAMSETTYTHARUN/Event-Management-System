from typing import Optional
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, examples=["Technology"])
    description: Optional[str] = Field(None, examples=["Events related to web development, AI, and hardware."])

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, examples=["Tech & Science"])
    description: Optional[str] = Field(None, examples=["Updated description."])

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
