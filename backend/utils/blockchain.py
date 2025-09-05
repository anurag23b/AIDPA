from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv
import json

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("ANVIL_URL")))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
TASK_STORAGE_ADDRESS = os.getenv("TASK_STORAGE_ADDRESS")

default_account = None
if PRIVATE_KEY:
    # Store original key for error reporting
    original_key = PRIVATE_KEY
    # Remove '0x' prefix if present and strip any trailing whitespace
    has_prefix = PRIVATE_KEY.startswith("0x")
    if has_prefix and len(original_key) == 66:
        PRIVATE_KEY = PRIVATE_KEY[2:]
    elif not has_prefix and len(original_key) == 64:
        pass  # No prefix to remove
    else:
        raise ValueError(f"Invalid PRIVATE_KEY format: {original_key} (expected 66 characters with '0x' or 64 hex characters)")
    PRIVATE_KEY = PRIVATE_KEY.strip()
    # Validate the hex portion (should be exactly 64 characters after prefix removal)
    if len(PRIVATE_KEY) != 64 or not all(c in '0123456789abcdefABCDEF' for c in PRIVATE_KEY):
        raise ValueError(f"Invalid PRIVATE_KEY format: {original_key} (expected 64 hex characters after '0x' removal)")
    private_key_bytes = bytes.fromhex(PRIVATE_KEY)
    default_account = Account.from_key(private_key_bytes).address

with open("utils/TaskStorage_abi.json") as f:
    contract_data = json.load(f)
    contract_abi = contract_data  # Use the list directly if ABI is a list

contract = w3.eth.contract(address=Web3.to_checksum_address(TASK_STORAGE_ADDRESS), abi=contract_abi)

def store_task(task_id: str, ipfs_hash: str):
    try:
        if not default_account:
            return "⚠️ No valid account to send transaction"
        txn = contract.functions.storeTask(task_id, ipfs_hash).build_transaction({
            'from': default_account,
            'nonce': w3.eth.get_transaction_count(default_account),
            'gas': 3000000,
            'gasPrice': w3.to_wei('1', 'gwei')
        })
        signed_txn = Account.sign_transaction(txn, private_key=private_key_bytes)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"❌ Blockchain/IPFS storage error: {e}")
        return f"⚠️ Could not store to blockchain: {str(e)}"

def retrieve_task(task_id: str) -> dict:
    try:
        task_count = contract.functions.getTaskCount().call()
        for i in range(task_count):
            task = contract.functions.getTask(i).call()
            if task[1] == task_id:
                return {"user": task[0], "taskId": task[1], "ipfsHash": task[2], "timestamp": task[3]}
        return {}
    except Exception as e:
        print(f"❌ Blockchain retrieval error: {e}")
        return {}