# schemas.py
from pydantic import BaseModel
from typing import Dict, Any

class SupplierIn(BaseModel):
    supplier_id: str
    name: str
    attributes: Dict[str, Any]

class SupplierRiskOut(BaseModel):
    supplier_id: str
    risk_score: float
    risk_label: str
