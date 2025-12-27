from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    id: Optional[int] = None  # optional for POST
    name: str
    age: int
    grade: str
    email: str
    courses: str

    class Config:
        orm_mode = True  # required to return SQLAlchemy objects directly
