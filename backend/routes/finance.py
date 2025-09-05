# backend/routes/finance.py (updated)
from fastapi import APIRouter, Depends, Body
from sqlmodel import Session, SQLModel, Field, select
from database import get_session
from datetime import datetime
import numpy as np

router = APIRouter(tags=["finance"])

class FinanceEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str
    amount: float
    category: str = Field(default="general")  # Default value
    timestamp: datetime = Field(default_factory=datetime.utcnow)

@router.post("/log")
def log_entry(entry: FinanceEntry, session: Session = Depends(get_session)):
    db_entry = FinanceEntry(**entry.dict(exclude_unset=True, exclude={"id"}))
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.get("/all")
def get_all(session: Session = Depends(get_session)):
    return session.exec(select(FinanceEntry).order_by(FinanceEntry.timestamp.desc())).all()

@router.get("/forecast")
def get_financial_forecast():
    months = ["July", "Aug", "Sep", "Oct", "Nov"]
    predicted_savings = [4000, 4200, 4400, 4600, 4800]
    predicted_expenses = [3000, 3200, 3100, 3300, 3400]
    return {
        "labels": months,
        "predicted_savings": predicted_savings,
        "predicted_expenses": predicted_expenses,
    }