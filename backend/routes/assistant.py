# backend/routes/assistant.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from agents.llm_chat import FreeLLMWrapper
from langchain_core.messages import HumanMessage
from sqlmodel import select
from database import get_session
from models.task import Task as TaskModel
from memory.vector_memory import get_task_vector_memory
from utils.mongo_client import get_assistant_collection
from datetime import datetime
from typing import Dict, List
from bson import ObjectId
import io
import base64
import speech_recognition as sr
import pyttsx3

router = APIRouter(tags=["assistant"])
llm = FreeLLMWrapper()

# Initialize pyttsx3 with error handling
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # Use the first available voice
    else:
        print("⚠️ No voices found, defaulting to silent mode for pyttsx3")
except Exception as e:
    print(f"⚠️ Failed to initialize pyttsx3: {e}, disabling voice synthesis")
    engine = None

class AskInput(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str

class VoiceInput(BaseModel):
    audio_data: str  # Base64-encoded audio

@router.get("/health")
def assistant_health():
    return {"status": "assistant routes are healthy"}

@router.post("/chat")
async def assistant_chat(req: ChatRequest):
    print("🧠 Chat input:", req.message)
    try:
        resp = llm.invoke([HumanMessage(content=req.message)])
        response_content = resp.content.strip()
        # Store in MongoDB
        collection = get_assistant_collection()
        await collection.insert_one({
            "user_id": "user123",  # Replace with proper user ID from header
            "role": "user",
            "content": req.message,
            "type": "general",
            "timestamp": datetime.utcnow()
        })
        await collection.insert_one({
            "user_id": "user123",
            "role": "assistant",
            "content": response_content,
            "type": "general",
            "timestamp": datetime.utcnow()
        })
        return {"response": response_content}
    except Exception as e:
        print("❌ Chat failed:", e)
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.post("/ask")
async def assistant_ask(input: AskInput, session=Depends(get_session)):
    try:
        tasks = session.exec(select(TaskModel)).all()
        task_text = "\n".join([f"{t.id}: {t.title} — {t.description or ''}" for t in tasks])
        prompt = f"Here are your tasks:\n{task_text}\n\nUser query: {input.query}"
        resp = llm.invoke([HumanMessage(content=prompt)])
        response_content = resp.content.strip()
        # Store in MongoDB
        collection = get_assistant_collection()
        await collection.insert_one({
            "user_id": "user123",  # Replace with proper user ID from header
            "role": "user",
            "content": input.query,
            "type": "general",
            "timestamp": datetime.utcnow()
        })
        await collection.insert_one({
            "user_id": "user123",
            "role": "assistant",
            "content": response_content,
            "type": "general",
            "timestamp": datetime.utcnow()
        })
        return {"response": response_content}
    except Exception as e:
        print("❌ Ask failed:", e)
        raise HTTPException(status_code=500, detail=f"Ask failed: {str(e)}")

@router.get("/history")
async def get_assistant_history():
    try:
        collection = get_assistant_collection()
        history = await collection.find({"user_id": "user123"}).to_list(length=100)
        # Convert ObjectId to string for JSON serialization
        return [{"_id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}} for doc in history]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@router.post("/voice")
async def assistant_voice(input: VoiceInput):
    try:
        # Decode base64 audio data
        audio_data = base64.b64decode(input.audio_data)
        with io.BytesIO(audio_data) as audio_file:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

        # Process with LLM
        resp = llm.invoke([HumanMessage(content=text)])
        response_content = resp.content.strip()

        # Convert response to audio if engine is available
        audio_response = None
        if engine:
            engine.save_to_file(response_content, "response.wav")
            engine.runAndWait()
            with open("response.wav", "rb") as f:
                audio_response = base64.b64encode(f.read()).decode("utf-8")
        else:
            print("⚠️ Skipping audio response due to pyttsx3 initialization failure")

        # Store in MongoDB
        collection = get_assistant_collection()
        await collection.insert_one({
            "user_id": "user123",  # Replace with proper user ID from header
            "role": "user",
            "content": text,
            "type": "voice",
            "timestamp": datetime.utcnow()
        })
        await collection.insert_one({
            "user_id": "user123",
            "role": "assistant",
            "content": response_content,
            "type": "voice",
            "timestamp": datetime.utcnow()
        })

        return {"response": response_content, "audio_response": audio_response}
    except Exception as e:
        print("❌ Voice failed:", e)
        raise HTTPException(status_code=500, detail=f"Voice failed: {str(e)}")