# backend/routes/health.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_session
from models.health_log import HealthLog
from schemas.health import AnalyzeHealthRequest, HealthInput, HealthRecord
import json
import logging
from utils.health import predict_health_score

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])

try:
    from utils.health import predict_health_score, generate_health_advice, analyze_lstm_health
    from utils.llm import llama3_health_advice
    from agents.health_chain import run_health_chain
    from utils.habit_learner import suggest_habits
    logger.info("Successfully imported health utilities")
except ImportError as e:
    logger.error("Failed to import health utilities: %s", str(e))
    raise HTTPException(status_code=500, detail=f"Service unavailable: {str(e)}")

@router.post("/analyze")
async def analyze_health(data: AnalyzeHealthRequest):
    logger.info("Received health analysis request: %s", data.models_dump())
    try:
        result = await run_health_chain(data.data)

        if isinstance(result, dict):
            parsed = result
        else:
            try:
                parsed = json.loads(result)
            except json.JSONDecodeError:
                status, chart = analyze_lstm_health(data.data)
                parsed = {"status": status, "recommendations": [], "chart": chart}

        if "chart" not in parsed:
            _, chart = analyze_lstm_health(data.data)
            parsed["chart"] = chart

        log = HealthLog(
            user_id="user123",
            input_text=data.data,
            status=parsed["status"],
            recommendations=parsed.get("recommendations", []),
            chart=json.dumps(parsed["chart"]),
        )
        db = SessionLocal()
        try:
            db.add(log)
            db.commit()
            db.refresh(log)
            logger.info("Health log saved with ID: %s", log.id)
        except Exception as db_error:
            db.rollback()
            logger.error("Failed to save health log: %s", str(db_error))
            raise HTTPException(status_code=500, detail="Failed to log health data")
        finally:
            db.close()

        return {
            "status": parsed["status"],
            "recommendations": parsed.get("recommendations", []),
            "chart": parsed["chart"]
        }
    except Exception as e:
        logger.error("Health analysis failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Health analysis failed: {str(e)}")

@router.get("/")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}

@router.post("/predict")
async def health_prediction(input_data: HealthInput, session: Session = Depends(get_session)):
    logger.info("Received health prediction request: %s", input_data.model_dump())
    try:
        # Extract records for prediction
        records_data = {"records": [r.model_dump() for r in input_data.records]}
        score = predict_health_score(records_data)
        return {"health_score": round(score, 2)}  # Return as percentage
    except Exception as e:
        logger.error("Health prediction failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/log")
def log_health(record: HealthRecord, db: Session = Depends(get_session)):
    logger.info("Received health log request: %s", record.model_dump())
    try:
        entry = HealthLog(**record.model_dump())
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {"message": "Health entry saved", "id": entry.id}
    except Exception as e:
        db.rollback()
        logger.error("Failed to log health entry: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
def get_logs(db: Session = Depends(get_session)):
    logger.info("Fetching health logs")
    try:
        logs = db.query(HealthLog).order_by(HealthLog.timestamp.desc()).limit(7).all()
        return logs
    except Exception as e:
        logger.error("Failed to fetch logs: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/advice")
async def get_health_advice(input_data: HealthInput):
    logger.info("Received health advice request: %s", input_data.model_dump())
    try:
        advice = await generate_health_advice(input_data.model_dump())
        return {"advice": advice}
    except Exception as e:
        logger.error("Health advice failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_health_history(user_id: str = "user123"):
    logger.info("Fetching health history for user: %s", user_id)
    db = SessionLocal()
    try:
        logs = db.query(HealthLog).filter_by(user_id=user_id).order_by(HealthLog.timestamp.desc()).all()
        return [{
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "input": log.input_text,
            "status": log.status,
            "recommendations": log.recommendations,
            "chart": log.chart
        } for log in logs]
    except Exception as e:
        logger.error("Failed to fetch history: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()