from datetime import datetime
from typing import List
from models.task import Task
from utils.llm import call_llm
import json
import dateparser
from fastapi import HTTPException  # needed for proper error signaling

def summarize_schedule(tasks: List[Task]) -> str:
    upcoming = sorted(
        [t for t in tasks if not t.completed and t.due_date],
        key=lambda x: x.due_date
    )
    if not tasks:
        return "No tasks to summarize."
    summary = "\n".join([f"{t.title}: {t.description}" for t in upcoming])
    return f"🗓️ Upcoming Schedule:\n{summary}"

def extract_schedule(nl_input: str):
    prompt = f"""
You are a helpful assistant that converts natural language into a structured task.
Extract the following from this user input:

1. title (short summary)
2. description (detailed if available)
3. due_date (ISO format e.g. "2025-07-06T09:00")
4. repeat (one of: "none", "daily", "weekly", "monthly")

User input: "{nl_input}"

Respond only in JSON. Example:
{{
  "title": "Take vitamins",
  "description": "Daily reminder to take vitamin D",
  "due_date": "2025-07-06T14:00:00",
  "repeat": "daily"
}}
"""

    raw = call_llm(prompt)
    try:
        parsed = json.loads(raw)

        # 🧠 Fix missing or null due_date using fallback
        if not parsed.get("due_date"):
            parsed_date = dateparser.parse(nl_input)
            if parsed_date:
                parsed["due_date"] = parsed_date.isoformat()
            else:
                raise HTTPException(status_code=400, detail="Missing or unparseable due_date.")

        return parsed

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode failed. Raw response: {raw}")
        raise HTTPException(status_code=400, detail="Invalid LLM output format.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal parsing error.")
