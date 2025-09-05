# backend/memory/vector_memory.py
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from storage.task_store import get_all_tasks

INDEX_NAME = "task_index"
VECTOR_DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../vector_memory/faiss_index")
)

def get_task_vector_memory():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    try:
        vector_store = FAISS.load_local(
            VECTOR_DB_PATH,
            embedding,
            allow_dangerous_deserialization=True
        )
        return vector_store.as_retriever()
    except Exception as e:
        print("⚠️ Failed to load FAISS index (will rebuild):", e)

    tasks = get_all_tasks()
    if not tasks:
        print("⚠️ No tasks found in storage; FAISS cannot be built.")
        return None

    documents = [Document(page_content=f"{t.get('taskId', str(uuid.uuid4()))}: {t.get('ipfsHash', '')}") for t in tasks]
    vector_store = FAISS.from_documents(documents, embedding)
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store.as_retriever()

def save_vector_memory():
    tasks = get_all_tasks()
    if not tasks:
        print("⚠️ No tasks to save.")
        return

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    documents = [Document(page_content=f"{t.get('taskId', str(uuid.uuid4()))}: {t.get('ipfsHash', '')}") for t in tasks]
    vector_store = FAISS.from_documents(documents, embedding)
    vector_store.save_local(VECTOR_DB_PATH)
    print("✅ Vector memory saved.")