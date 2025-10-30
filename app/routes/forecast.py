# routes/forecast.py
from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
from io import StringIO
from app.ml.demand_forecast import train_and_forecast

router = APIRouter()

@router.post("/forecast_csv")
async def forecast_csv(file: UploadFile = File(...), steps: int = 12):
    contents = await file.read()
    s = contents.decode("utf-8")
    df = pd.read_csv(StringIO(s), parse_dates=[0], index_col=0)
    # assume df is single column timeseries
    if df.shape[1] > 1:
        raise HTTPException(status_code=400, detail="Expect single series")
    series = df.iloc[:,0].astype(float)
    res = train_and_forecast(series, steps=steps)
    return res
