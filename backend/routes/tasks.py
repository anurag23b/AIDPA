# backend/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Request, Body, Query
from sqlmodel import Session, select, col
from sqlalchemy import or_, and_, cast, String
from models.task import Task
from database import get_session
from typing import List, Optional
from utils.habit_learner import adjust_repeat_schedule
from utils.scheduler import summarize_schedule
from utils.ipfs import store_task_on_ipfs
from datetime import datetime
from routes.nlp import extract_task_from_text, summarize_tasks
from models.task_update import TaskUpdate
from collections import Counter
from utils.blockchain import store_task
from uuid import UUID
from agents.task_chain import run_task_chain

router = APIRouter()

@router.get("", response_model=List[Task])  # Handle /api/tasks
@router.get("/", response_model=List[Task])  # Handle /api/tasks/
def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due_before: Optional[str] = None,
    tag: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    session: Session = Depends(get_session)
):
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority:
        query = query.where(Task.priority == priority)
    if category:
        query = query.where(Task.category == category)
    if due_before:
        try:
            due_date_limit = datetime.fromisoformat(due_before)
            query = query.where(Task.due_date != None).where(Task.due_date < due_date_limit)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid date format for 'due_before'")
    if tag:
        query = query.where(Task.tags != None).where(cast(Task.tags, String).like(f'%"{tag}"%'))
    if sort_by:
        sort_col = getattr(Task, sort_by, None)
        if sort_col:
            query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())
    tasks = session.exec(query).all()
    return tasks

@router.post("", response_model=Task)  # Handle /api/tasks
@router.post("/", response_model=Task)  # Handle /api/tasks/
def create_task(task_data: dict = Body(...), session: Session = Depends(get_session)):
    task_data.pop("id", None)
    if "due_date" in task_data and isinstance(task_data["due_date"], str):
        try:
            task_data["due_date"] = datetime.fromisoformat(task_data["due_date"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    task = Task(**task_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    try:
        task_dict = task.model_dump()
        task_dict["due_date"] = task_dict["due_date"].isoformat() if task_dict["due_date"] else None
        ipfs_hash = store_task_on_ipfs(task_dict)
        store_task(str(task.id), ipfs_hash)
        print(f"✅ Task stored on IPFS + Blockchain: {ipfs_hash}")
    except Exception as e:
        print(f"⚠️ Blockchain/IPFS storage failed: {e}")
    return task

@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_data: TaskUpdate = Body(...), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "due_date" and isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
        setattr(task, key, value)
    try:
        session.commit()
        session.refresh(task)  # Ensure the task is refreshed
        task_dict = task.model_dump()
        task_dict["due_date"] = task_dict["due_date"].isoformat() if task_dict["due_date"] else None
        if task.completed and task.repeat and task.repeat != "none":
            from utils.habit_learner import get_next_due_date
            next_due = get_next_due_date(task.due_date or datetime.now(), task.repeat)
            if next_due:
                new_task = Task(
                    title=task.title,
                    description=task.description,
                    completed=False,
                    priority=task.priority,
                    category=task.category,
                    due_date=next_due,
                    repeat=task.repeat,
                    tags=task.tags
                )
                session.add(new_task)
                session.commit()
                session.refresh(new_task)
        return task  # Return the refreshed task object
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@router.delete("/{task_id}")
def delete_task(task_id: UUID, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@router.post("/parse", response_model=Task)
async def create_task_from_text(request: Request, session: Session = Depends(get_session)):
    body = await request.json()
    print("📥 Raw request body:", body)
    raw_input = body.get("raw_input")
    if not raw_input or not isinstance(raw_input, str):
        raise HTTPException(status_code=400, detail="Invalid or missing 'raw_input'")
    
    task_data = await extract_task_from_text(raw_input)
    print("🤖 NLP returned:", task_data)
    
    if not isinstance(task_data, dict) or not task_data.get("title"):
        raise HTTPException(status_code=400, detail=f"Missing or empty task title: {task_data}")
    
    if isinstance(task_data, str):
        try:
            import json
            task_data = json.loads(task_data)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid NLP response format: {e}")

    task_data.setdefault("description", "")
    task_data.setdefault("repeat", "none")
    task_data.setdefault("priority", "normal")
    task_data.setdefault("category", "general")
    task_data.setdefault("completed", False)
    task_data.setdefault("schedule", "daily")
    
    task_data = adjust_repeat_schedule(task_data)
    task_data.pop("id", None)
    
    if task_data.get("due_date"):
        try:
            parsed = datetime.fromisoformat(task_data["due_date"])
            if parsed < datetime.now():
                parsed = parsed.replace(year=datetime.now().year)
                task_data["due_date"] = parsed.isoformat()
        except (ValueError, TypeError):
            task_data["due_date"] = datetime.now().isoformat()
    
    try:
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        task_dict = {k: v.isoformat() if isinstance(v, datetime) else v for k, v in task.model_dump().items()}
        ipfs_hash = store_task_on_ipfs(task_dict)
        store_task(str(task.id), ipfs_hash)
        print(f"✅ Task stored on IPFS + Blockchain: {ipfs_hash}")
        
        return task
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save task: {str(e)}")

@router.get("/summary")
def get_task_summary(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    now = datetime.now()
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.completed])
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < now and not t.completed])
    category_counts = Counter([t.category or "uncategorized" for t in tasks])
    tag_counts = Counter(tag for t in tasks if t.tags for tag in t.tags)
    summary = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "category_breakdown": category_counts,
        "tag_breakdown": tag_counts,
    }
    task_dicts = [t.model_dump() for t in tasks]
    summary["nlp_summary"] = summarize_tasks(task_dicts)
    return summary

@router.post("/optimize")
async def optimize_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    task_dicts = [t.model_dump() for t in tasks]
    optimized = await run_task_chain(task_dicts)
    return {"optimized_tasks": optimized}