# backend/scripts/insert_dummy_tasks.py
from storage.task_store import save_task

save_task({"taskId": "Test task 1", "ipfsHash": "QmDummyHash1"})
save_task({"taskId": "Test task 2", "ipfsHash": "QmDummyHash2"})

print("✅ Dummy tasks added")
