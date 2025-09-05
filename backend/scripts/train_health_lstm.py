# backend/scripts/train_health_lstm.py
import torch
import torch.nn as nn
import numpy as np
from backend.models.health_lstm import HealthLSTM  # Adjusted import
from utils.mongo_client import get_health_collection
import asyncio

async def fetch_health_data():
    try:
        collection = get_health_collection()
        records = await collection.find({"user_id": "user123"}).to_list(length=100)
        data = [
            {
                "steps": r.get("records", [{}])[0].get("steps", 0),
                "heart_rate": r.get("records", [{}])[0].get("heart_rate", 0),
                "sleep_hours": r.get("records", [{}])[0].get("sleep_hours", 0)
            }
            for r in records if r.get("records")
        ]
        return data if data else [
            {"steps": 8000, "heart_rate": 70, "sleep_hours": 7.5},
            {"steps": 6000, "heart_rate": 75, "sleep_hours": 6.0},
            {"steps": 9000, "heart_rate": 68, "sleep_hours": 8.0}
        ]
    except Exception as e:
        print(f"❌ Failed to fetch health data: {e}")
        return [
            {"steps": 8000, "heart_rate": 70, "sleep_hours": 7.5},
            {"steps": 6000, "heart_rate": 75, "sleep_hours": 6.0},
            {"steps": 9000, "heart_rate": 68, "sleep_hours": 8.0}
        ]

def main():
    data = asyncio.run(fetch_health_data())
    sequences = np.array([[d["steps"]/10000, d["heart_rate"]/100, d["sleep_hours"]/8] for d in data])
    label = 1 if np.mean([d["steps"] for d in data]) > 7000 and np.mean([d["sleep_hours"] for d in data]) > 6 else 0
    
    model = HealthLSTM(input_size=3, hidden_size=64, num_layers=2, output_size=1)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(100):
        inputs = torch.tensor(sequences, dtype=torch.float32).unsqueeze(0)
        targets = torch.tensor([[label]], dtype=torch.float32)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    torch.save(model.state_dict(), "backend/models/health_lstm.pth")
    print("✅ Model trained and saved")

if __name__ == "__main__":
    main()