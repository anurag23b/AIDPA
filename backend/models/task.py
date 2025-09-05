from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
import json

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "normal"
    category: Optional[str] = "general"
    completed: Optional[bool] = False
    due_date: Optional[datetime] = None
    repeat: Optional[str] = "none"
    schedule: Optional[str] = "daily"

    # ✅ Serialize list as string (stored as TEXT in DB)
    tags: Optional[str] = Field(default_factory=lambda: json.dumps([]))
