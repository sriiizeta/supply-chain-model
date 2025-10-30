# backend/app/ml/supplier_risk.py
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# base directory of this file (robust)
BASE_DIR = Path(__file__).resolve().parent

# model filename stored next to this file
MODEL_PATH = BASE_DIR / "supplier_risk_model.joblib"

FEATURE_COLS = [
    "lead_time_mean",
    "lead_time_std",
    "defect_rate",
    "late_shipments_rate",
    "financial_score",
]

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Selects feature columns and fills missing values with 0."""
    # ensure all feature cols exist (missing ones will be filled with zeros)
    for c in FEATURE_COLS:
        if c not in df.columns:
            df[c] = 0
    features = df[FEATURE_COLS].fillna(0)
    return features

def train_supplier_risk(df: pd.DataFrame, target_col: str = "risk_label_numeric") -> RandomForestRegressor:
    """
    Train a RandomForestRegressor and persist it to MODEL_PATH.
    Expects df to contain FEATURE_COLS and the target_col.
    """
    if target_col not in df.columns:
        raise RuntimeError(f"Training CSV must include the target column '{target_col}'.")

    X = build_features(df)
    y = df[target_col]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    # Ensure model directory exists and dump model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model

def load_model() -> Optional[RandomForestRegressor]:
    """Load model if it exists; otherwise return None."""
    try:
        if MODEL_PATH.exists():
            return joblib.load(MODEL_PATH)
    except Exception as exc:
        # you can log exc if you have logging in the project
        pass
    return None

def predict_risk_from_attributes(attributes: Dict) -> Dict:
    """
    Predict risk score and label from a dictionary of attributes.
    Raises RuntimeError if no trained model is available.
    """
    model = load_model()
    if model is None:
        raise RuntimeError("Model not trained yet. Please POST a training CSV to /train_supplier_model first.")

    # build a single-row dataframe with required columns
    row = {c: float(attributes.get(c, 0.0) or 0.0) for c in FEATURE_COLS}
    X = pd.DataFrame([row], columns=FEATURE_COLS)

    # predict — regressor returns a numeric score
    try:
        score = float(model.predict(X)[0])
    except Exception as exc:
        raise RuntimeError(f"Model prediction failed: {exc}")

    # convert numeric score to label thresholds (adjust thresholds if desired)
    label = "High" if score > 0.66 else ("Medium" if score > 0.33 else "Low")

    return {"risk_score": score, "risk_label": label}
