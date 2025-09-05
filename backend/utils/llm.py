# backend/utils/llm.py
from datetime import datetime
from langchain_core.messages import HumanMessage
from agents.llm_chat import FreeLLMWrapper

llm = FreeLLMWrapper()

def call_llm(prompt, model="mistral"):
    res = llm.invoke([HumanMessage(content=prompt)])
    return res.content.strip()

def summarize_tasks(tasks):
    if not tasks:
        return "🎉 You're all caught up! No tasks right now."

    upcoming_tasks = [t for t in tasks if not t.get("completed") and t.get("due_date")]
    upcoming_tasks.sort(key=lambda x: x["due_date"])

    summary_lines = [f"You have {len(tasks)} tasks in total."]

    if upcoming_tasks:
        summary_lines.append("Here are the next few tasks:")
        for t in upcoming_tasks[:3]:
            due = datetime.fromisoformat(t["due_date"]).strftime("%b %d, %I:%M %p")
            summary_lines.append(f"• {t['title']} — due {due}")
    else:
        summary_lines.append("No upcoming tasks with due dates.")

    return "\n".join(summary_lines)

def llama3_health_advice(text: str):
    return [
        "Try to get at least 7-8 hours of sleep.",
        "Consider mindfulness meditation to reduce stress.",
        "Drink at least 2L of water daily."
    ]
