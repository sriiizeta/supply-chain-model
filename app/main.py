# main.py
from fastapi import FastAPI
from app.routes import risk, forecast
from app.db import Base, engine
from app import models

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SCRM MVP")

app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])

@app.get("/health")
def health():
    return {"status": "ok"}
