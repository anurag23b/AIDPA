import json
import httpx
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
import re

async def run_task_chain(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    task_str = ""
    for i, task in enumerate(tasks, 1):
        task_str += f"{i}. Title: {task['title']}, Priority: {task.get('priority')}, Due: {task.get('due_date')}, Completed: {task.get('completed', False)}, Repeat: {task.get('repeat', 'none')}\n"

    prompt = f"""
    You are a smart productivity assistant. Reprioritize tasks based on:
    - Urgency: exams or deadlines within 2 days → high
    - Health tasks → medium
    - Daily habits → low
    - Overdue tasks: suggest new due dates (tomorrow for high, next week for others)
    - Add 'suggested_action': keep | reschedule | delete (delete if >30 days overdue)

    Respond in JSON:
    [
        {
            "title": "...",
            "priority": "...",
            "due_date": "...",
            "repeat": "...",
            "completed": false,
            "suggested_action": "..."
        }
    ]

    TASKS:
    {task_str}
    """

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            match = re.search(r"\[\s*{[\s\S]*?}\s*]", content)
            if match:
                return json.loads(match.group())
            return []
        except Exception as e:
            print(f"❌ TaskChain error: {e}")
            return []