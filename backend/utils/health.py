import torch
import numpy as np
from models.health_lstm import HealthLSTM
import httpx
import random
from datetime import datetime, timedelta


# Load model
model = HealthLSTM(input_size=3)
model.load_state_dict(torch.load("models/health_lstm.pth", map_location=torch.device("cpu")))
model.eval()

def preprocess_health_data(data: dict) -> torch.Tensor:
    """
    Accepts a dict of historical health records, returns a 3D tensor:
    shape = (1, sequence_length, num_features)
    """
    # Assume input: list of dicts, each with 'steps', 'heart_rate', 'sleep_hours'
    sequence = [[d["steps"], d["heart_rate"], d["sleep_hours"]] for d in data["records"]]
    arr = np.array(sequence, dtype=np.float32)
    tensor = torch.tensor(arr).unsqueeze(0)  # Add batch dimension
    return tensor

def predict_health_score(data: dict) -> float:
    """
    Calculate health score (0–100) from rule-based model.
    """
    records = data["records"]
    total_score = 0

    for record in records:
        steps = record["steps"]
        hr = record["heart_rate"]
        sleep = record["sleep_hours"]

        # Normalize each feature
        step_score = min(steps / 10000, 1.0)
        hr_score = 1.0 if 60 <= hr <= 80 else max(0, 1 - abs(70 - hr) / 30)
        sleep_score = min(sleep / 8.0, 1.0)

        record_score = (step_score + hr_score + sleep_score) / 3
        total_score += record_score

    average_score = total_score / len(records)
    return round(average_score * 100, 4)  # convert to 0–100 scale

async def generate_health_advice(data):
    import traceback

    try:
        records = data.get("records", [])
        prompt = "You are a helpful AI health assistant. The user has logged their recent health metrics:\n\n"

        for i, rec in enumerate(records):
            prompt += f"Day {i+1}: Steps={rec.get('steps')}, Heart Rate={rec.get('heart_rate')}, Sleep Hours={rec.get('sleep_hours')}\n"

        prompt += f"\nUser also reported: {data.get('data')}\n"
        prompt += "\nBased on the above, provide personalized health suggestions:\n"

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                }
            )

            print("📨 Response status code:", response.status_code)
            print("📨 Response content-type:", response.headers.get("content-type"))
            print("📨 Response body:\n", response.text)

            response.raise_for_status()

            json_data = response.json()
            print("🟢 Parsed JSON from Ollama:", json_data)

            return json_data["message"]["content"]

    except Exception as e:
        print("❌ Exception in generate_health_advice:")
        traceback.print_exc()
        return [f"⚠️ Error contacting LLaMA: {repr(e)}"]

def analyze_lstm_health(text: str):
    # Placeholder ML analysis
    status = "You seem to be under mild stress with irregular sleep."

    # Simulated trend data
    today = datetime.utcnow()
    chart = [
        {"date": (today - timedelta(days=i)).strftime("%Y-%m-%d"), "value": random.randint(60, 100)}
        for i in range(7)
    ]
    return status, list(reversed(chart))
