# backend/main.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware import Middleware
from starlette.requests import HTTPConnection
from database import create_db_and_tables, Base, engine
from dotenv import load_dotenv
import logging

load_dotenv()
app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None)  # Disable auto-redirects
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware to trust proxy headers and influence redirects
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["aidpa.local", "*.aidpa.local"]),
    Middleware(CORSMiddleware, allow_origins=["https://aidpa.local"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
]

# Custom middleware to set scheme from X-Forwarded-Proto and fix redirect Location
@app.middleware("http")
async def trust_proxy_headers(request: Request, call_next):
    if "X-Forwarded-Proto" in request.headers:
        scheme = request.headers["X-Forwarded-Proto"]
        logger.info(f"Detected scheme from X-Forwarded-Proto: {scheme}")
        url = request.url.replace(scheme=scheme)
        request._url = url
        request.scope["scheme"] = scheme
    response = await call_next(request)
    if response.status_code == 307 and "Location" in response.headers:
        location = response.headers["Location"]
        logger.info(f"Original Location header: {location}")
        if location.startswith("http://"):
            new_location = location.replace("http://", f"https://{request.url.host}", 1)
            response.headers["Location"] = new_location
            logger.info(f"Updated Location header to: {new_location}")
    return response

app = FastAPI(middleware=middleware)

Base.metadata.create_all(bind=engine)

try:
    from routes import tasks, scheduler, health, nlp, assistant, habits
    import routes.finance as finance
    app.include_router(tasks.router, prefix="/api/tasks")
    app.include_router(scheduler.router, prefix="/api")
    app.include_router(health.router, prefix="/api/health")
    app.include_router(habits.router, prefix="/api/habits")
    app.include_router(nlp.router, prefix="/api/nlp")
    app.include_router(assistant.router, prefix="/api/assistant")
    app.include_router(finance.router, prefix="/api/finance")
    logger.info("All routers loaded: tasks=%s, health=%s, habits=%s", tasks.router.routes, health.router.routes, habits.router.routes)
    print("Registered routes:", [r.path for r in app.routes])
except Exception as e:
    logger.error("Failed to include routers: %s", str(e), exc_info=True)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root(request: Request):
    return {"message": "AIDPA Backend Running", "scheme": request.url.scheme}

@app.get("/health")
def health_check():
    return {"status": "healthy", "time": "05:32 PM IST, August 06, 2025"}

@app.get("/api/llm/health")
def openrouter_health():
    import requests
    try:
        r = requests.get("https://openrouter.ai")
        return {"openrouter_status": "running" if r.ok else "not responding"}
    except:
        return {"openrouter_status": "down"}