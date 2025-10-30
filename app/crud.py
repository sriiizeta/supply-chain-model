# crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date

def get_supplier(db: Session, supplier_id: str):
    return db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()

def create_supplier(db: Session, supplier: schemas.SupplierIn):
    db_obj = models.Supplier(
        supplier_id=supplier.supplier_id,
        name=supplier.name,
        attributes=supplier.attributes
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def save_forecast(db: Session, series_name: str, result: dict):
    obj = models.ForecastResult(created_at=date.today(), series_name=series_name, result=result)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj