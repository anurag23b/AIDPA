from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    repeat: Optional[str] = None
    schedule: Optional[str] = None
