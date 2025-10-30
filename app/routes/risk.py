# routes/risk.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from app.schemas import SupplierIn, SupplierRiskOut
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app import crud
from app.ml.supplier_risk import predict_risk_from_attributes, train_supplier_risk
import pandas as pd
from io import StringIO

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/supplier", response_model=SupplierRiskOut)
def add_supplier_and_score(sup: SupplierIn, db: Session = Depends(get_db)):
    crud.create_supplier(db, sup)
    try:
        out = predict_risk_from_attributes(sup.attributes)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"supplier_id": sup.supplier_id, "risk_score": out["risk_score"], "risk_label": out["risk_label"]}

@router.post("/train_supplier_model")
async def train_model(file: UploadFile = File(...)):
    """
    Upload a CSV file containing supplier data to train the risk model.
    The CSV should include the necessary columns expected by train_supplier_risk().
    """
    try:
        contents = await file.read()
        s = contents.decode("utf-8")
        df = pd.read_csv(StringIO(s))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")

    try:
        model = train_supplier_risk(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error training model: {e}")

    return {"status": "trained", "n_rows": len(df)}