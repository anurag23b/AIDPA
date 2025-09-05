# backend/storage/task_store.py
import json
from pathlib import Path
from datetime import datetime
from models.task import Task
from database import SessionLocal

TASK_FILE = Path("storage/tasks.json")
TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
if not TASK_FILE.exists():
    TASK_FILE.write_text("[]")

def create_task(task_data):
    db = SessionLocal()
    if "due_date" not in task_data:
        task_data["due_date"] = datetime.now().isoformat()
    task = Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return task

def load_tasks():
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_task(task: dict):
    task["created_at"] = datetime.utcnow().isoformat()
    if "due_date" not in task:
        task["due_date"] = datetime.now().isoformat()
    tasks = load_tasks()
    tasks.append(task)
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def get_all_tasks():
    return load_tasks()
