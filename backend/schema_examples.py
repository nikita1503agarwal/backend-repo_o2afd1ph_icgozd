from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas to guide new collections

class User(BaseModel):
    name: str
    email: str
    role: str = Field(default="citizen", description="citizen | lawyer | business")

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class Post(BaseModel):
    title: str
    body: str
    tags: List[str] = []

class Task(BaseModel):
    title: str
    completed: bool = False
