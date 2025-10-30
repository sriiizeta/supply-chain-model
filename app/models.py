# models.py
from sqlalchemy import Column, Integer, String, Float, Date, JSON
from app.db import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, unique=True, index=True)
    name = Column(String)
    attributes = Column(JSON)  # store metrics like lead_time_mean, defects_rate

class ForecastResult(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date)
    series_name = Column(String)
    result = Column(JSON)
