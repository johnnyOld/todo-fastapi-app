from pydantic import BaseModel
from datetime import datetime

class ToDoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 1

class ToDoCreate(ToDoBase):
    pass

class ToDoInDB(ToDoBase):
    id: int
    created_at: datetime
    due_date: datetime | None = None
    user_id: int

    class Config:
        orm_mode = True