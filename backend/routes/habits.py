# backend/routes/habits.py
from fastapi import APIRouter, HTTPException, Depends
from database import get_session
from sqlalchemy.orm import Session
from utils.habit_learner import suggest_habits
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["habits"])  # Removed prefix="/api/habits"

# Debug print to confirm loading
print("Habits router loaded")

try:
    # Pre-load Task model to catch import errors during setup
    from models.task import Task
    logger.info("Task model imported successfully")
except ImportError as e:
    logger.error("Failed to import Task model during router setup: %s", str(e), exc_info=True)
    raise  # This will fail fast and log the issue

@router.get("/suggest")
async def habit_suggestions(session: Session = Depends(get_session)):
    logger.info("Habit suggestions endpoint called")
    try:
        tasks = session.query(Task).all()  # Fetch all tasks
        logger.debug("Retrieved %d tasks from database: %s", len(tasks), [t.title for t in tasks[:2]])
        if not tasks:
            logger.warning("No tasks found in the database")
            return {"recommendations": ["No tasks available to suggest habits."]}

        # Convert Task objects to dictionaries with explicit attribute mapping
        task_dicts = [
            {
                "title": getattr(task, "title", "Untitled"),
                "category": getattr(task, "category", "general"),
                "completed": getattr(task, "completed", False),
                "due_date": getattr(task, "due_date", None)
            }
            for task in tasks
        ]
        logger.debug("Converted tasks to dictionaries: %s", task_dicts[:2])  # Log first two for brevity
        result = suggest_habits(task_dicts)
        logger.info("Habit suggestions generated: %s", result["recommendations"])
        return result
    except Exception as e:
        logger.error("Failed to generate habit suggestions: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate habit suggestions: {str(e)}")