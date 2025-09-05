# backend/routes/nlp.py
import json, re
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, HTTPException
from langchain_core.messages import HumanMessage
from agents.llm_chat import FreeLLMWrapper

router = APIRouter()
llm = FreeLLMWrapper()

def convert_special_types(data):
    if isinstance(data, dict):
        return {k: convert_special_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_special_types(item) for item in data]
    elif isinstance(data, uuid.UUID):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    return data

@router.post("/task")
async def extract_task_from_text(text: str = Body(...)):
    current_date = datetime.now()
    next_month = current_date.replace(day=1) + timedelta(days=32)
    next_month_start = next_month.replace(day=1)
    third_week_start = next_month_start + timedelta(days=14)  # 3rd week starts on day 15
    third_week_end = third_week_start + timedelta(days=6)    # End of 3rd week

    prompt = f"""Extract a task from this input:
'{text}'

Return only a valid JSON object with no preamble or explanation.

Fields:
- title (mandatory)
- due_date (ISO8601 or null; if '3rd week of next month' is specified, set to a date between {third_week_start.isoformat()} and {third_week_end.isoformat()} based on today {current_date.isoformat()}; if no year is specified, assume {current_date.year})
- priority: 'low', 'medium', or 'high'
- category: like 'work', 'health', 'personal'
- repeat: optional ('daily', 'weekly', etc.)

Example:
{{"title": "Important exam", "due_date": "2025-08-20T18:00:00", "priority": "high", "category": "study"}}
"""

    try:
        res = llm.invoke([HumanMessage(content=prompt)])
        full_response = res.content.strip()
        print("🧠 Raw LLM Response:\n", full_response)

        matches = re.findall(r'\{.*?\}', full_response, re.DOTALL)
        if not matches:
            raise HTTPException(status_code=400, detail=f"LLM response doesn't contain valid JSON: {full_response}")

        json_str = matches[-1]
        task_data = json.loads(json_str)
        if not isinstance(task_data, dict) or not task_data.get("title"):
            raise HTTPException(status_code=400, detail="Invalid or missing task title")

        # Force current year if due_date lacks it
        if task_data.get("due_date"):
            try:
                parsed = datetime.fromisoformat(task_data["due_date"])
                if not parsed.year or parsed.year < 2020:
                    parsed = parsed.replace(year=current_date.year)
                    task_data["due_date"] = parsed.isoformat()
            except ValueError:
                parsed = datetime.strptime(task_data["due_date"], "%Y-%m-%d")
                if not parsed.year or parsed.year < 2020:
                    parsed = parsed.replace(year=current_date.year)
                    task_data["due_date"] = parsed.isoformat()

        return task_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")

def summarize_tasks(tasks: list[dict]) -> str:
    if not tasks:
        return "You have no tasks at the moment."

    prompt = f"""
Given the following tasks, summarize the user's overall progress, patterns, or habits in 2-3 sentences. Focus on consistency, missed or overdue tasks, and category trends.

TASKS:
{json.dumps(convert_special_types(tasks), indent=2)}

Respond with a short paragraph in plain English.
"""
    try:
        res = llm.invoke([HumanMessage(content=prompt)])
        return res.content.strip()
    except Exception as e:
        return f"LLM summarization failed: {str(e)}"