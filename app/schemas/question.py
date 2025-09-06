from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config: from_attributes = True

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=255)
    answer: str = Field(..., min_length=1, max_length=255)
    category_id: Optional[int] = None

class QuestionResponse(BaseModel):
    id: int
    text: str
    answer: str
    category: Optional[CategoryResponse] = None
    class Config: from_attributes = True
