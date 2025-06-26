from fastapi import FastAPI
from .database import engine,Base
from .routes import factadmetricasdaily,dimension
import app.models
from .scheduler import start_scheduler

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    print("[STARTUP] Starting scheduler...")
    start_scheduler()

# Include routers
app.include_router(factadmetricasdaily.router,tags=['metrics'])
app.include_router(dimension.router,tags=['dimension'])