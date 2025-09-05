# backend/utils/habit_learner.py
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict

class HabitRL:
    def __init__(self, actions=["high", "medium", "low"]):
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.actions = actions
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.2  # Increased exploration rate

    def get_action(self, state: str) -> str:
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def update(self, state: str, action: str, reward: float, next_state: str):
        action_idx = self.actions.index(action)
        current_q = self.q_table[state][action_idx]
        next_max_q = np.max(self.q_table[next_state])
        self.q_table[state][action_idx] += self.alpha * (reward + self.gamma * next_max_q - current_q)

def suggest_habits(tasks: List[Dict]) -> Dict:
    rl = HabitRL()
    recommendations = []
    seen_titles = set()
    for task in tasks:
        title = task.get("title", "Untitled")
        if title in seen_titles:
            continue
        seen_titles.add(title)
        state = f"{task.get('category', 'general')}_{title}"
        due_date_str = task.get("due_date")
        due_date = datetime.fromisoformat(due_date_str) if due_date_str and isinstance(due_date_str, str) else None
        now = datetime.now()
        # Enhanced reward logic
        if due_date and due_date < now:
            reward = -3  # Strong penalty for overdue
        elif task.get("category", "general") == "health":
            reward = 2  # Higher reward for health
        elif due_date and (due_date - now).days <= 2:
            reward = 3  # High reward for urgent
        elif task.get("category", "general") in ["personal", "work"]:
            reward = 1  # Moderate reward for other categories
        else:
            reward = -1  # Default low reward
        action = rl.get_action(state)
        next_state = state
        rl.update(state, action, reward, next_state)
        recommendations.append(f"Set '{title}' to {action} priority.")
    return {"recommendations": recommendations}

def adjust_repeat_schedule(task_data: Dict) -> Dict:
    """Adjust repeat and schedule based on task data."""
    repeat = task_data.get("repeat", "none")
    schedule = task_data.get("schedule", "daily")
    if repeat != "none" and schedule == "daily":
        task_data["schedule"] = "weekly"
    return task_data

def get_next_due_date(current_due: datetime, repeat: str) -> datetime:
    """Calculate the next due date based on repeat schedule."""
    if repeat == "daily":
        return current_due + timedelta(days=1)
    elif repeat == "weekly":
        return current_due + timedelta(weeks=1)
    elif repeat == "monthly":
        return current_due + timedelta(days=30)
    return None