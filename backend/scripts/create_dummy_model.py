import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.health_lstm import HealthLSTM
import torch

model = HealthLSTM(input_size=3)
torch.save(model.state_dict(), "models/health_lstm.pth")
print("✅ Dummy model saved")