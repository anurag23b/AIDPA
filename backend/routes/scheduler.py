from fastapi import APIRouter
from pydantic import BaseModel, validator
from typing import List
from utils.llm import summarize_tasks
from datetime import datetime
from utils.scheduler import extract_schedule
from storage.task_store import create_task
import dateparser  # ✅ Needed to parse natural language dates

router = APIRouter()

class Task(BaseModel):
    title: str
    due_date: datetime
    description: str

    @validator("due_date", pre=True)
    def parse_due_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                # Parse natural language and default to current year
                parsed = dateparser.parse(value, settings={'PREFER_DAY_OF_MONTH': 'first', 'RETURN_AS_TIMEZONE_AWARE': False})
                if parsed:
                    if not parsed.year or parsed.year < 2020:  # Avoid old years
                        parsed = parsed.replace(year=datetime.now().year)
                    return parsed
                return datetime.now()
        return value

class TextInput(BaseModel):
    raw_input: str

@router.post("/tasks/parse")
def parse_task(data: TextInput):
    print("▶ Received input:", data.raw_input)
    parsed = extract_schedule(data.raw_input)
    print("✅ Extracted:", parsed)

    task = create_task(
        parsed["title"],
        parsed.get("description", ""),
        parsed["due_date"],
        parsed.get("repeat", "none")
    )
    return task

class TaskList(BaseModel):
    tasks: List[Task]

@router.post("/schedule/summary")
def summarize_schedule(data: TaskList):
    summary = summarize_tasks(data.tasks)
    return {"summary": summary}