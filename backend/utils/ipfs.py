# backend/utils/ipfs.py
import hashlib
import os
import ipfshttpclient
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()
IPFS_NODE_URL = os.getenv("IPFS_NODE_URL", "/dns4/ipfs-service/tcp/5001")

try:
    client = ipfshttpclient.connect(IPFS_NODE_URL)
except Exception as e:
    print(f"⚠️ Failed to connect to IPFS at {IPFS_NODE_URL}: {str(e)}")
    client = None

def hash_task_data(task_data: dict) -> str:
    # Convert datetime and UUID to string for hashing
    task_data_copy = {k: str(v) if isinstance(v, (datetime, uuid.UUID)) else v for k, v in task_data.items()}
    return hashlib.sha256(str(task_data_copy).encode()).hexdigest()

def store_task_on_ipfs(task_data: dict) -> str:
    if not client:
        print("✅ Task stored on IPFS + Blockchain: IPFS_DISABLED")
        return "IPFS_DISABLED"
    try:
        # Convert datetime and UUID to strings
        task_data_copy = {k: str(v) if isinstance(v, (datetime, uuid.UUID)) else v for k, v in task_data.items()}
        ipfs_response = client.add_json({
            "task_hash": hash_task_data(task_data),
            "task": task_data_copy
        })
        print(f"✅ Stored on IPFS: {ipfs_response}")
        return ipfs_response
    except Exception as e:
        print(f"⚠️ Failed to connect to IPFS: {e}")
        return "IPFS_DISABLED"

def retrieve_task_from_ipfs(ipfs_hash: str) -> dict:
    if not client:
        return {}
    try:
        return client.get_json(ipfs_hash)
    except Exception as e:
        print(f"⚠️ Failed to retrieve from IPFS: {e}")
        return {}