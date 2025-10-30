# demand_forecast.py
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from app.db import SessionLocal
from app.crud import save_forecast
import json
from datetime import date

def train_and_forecast(series: pd.Series, order=(1,1,0), seasonal_order=(0,0,0,0), steps=12):
    """
    series: pd.Series indexed by datetime (monthly/weekly)
    returns forecast dict with mean and conf intervals
    """
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    res = model.fit(disp=False)
    fc = res.get_forecast(steps=steps)
    mean = fc.predicted_mean
    conf = fc.conf_int()
    result = {
        "forecast_mean": mean.tolist(),
        "lower": conf.iloc[:,0].tolist(),
        "upper": conf.iloc[:,1].tolist(),
        "index": [str(d) for d in mean.index]
    }
    # optionally persist
    db = SessionLocal()
    save_forecast(db, series_name="demand_series", result=result)
    db.close()
    return result

# fallback simple ML regressor example
from sklearn.ensemble import RandomForestRegressor
def ml_forecast(X_train, y_train, X_pred):
    m = RandomForestRegressor(n_estimators=100)
    m.fit(X_train, y_train)
    return m.predict(X_pred)
