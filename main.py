from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(root_path="/docs")

(model, threshold) = joblib.load('model/condiciones_ambientales_gmm.joblib')

class DataPoint(BaseModel):
    temp: float
    hum: float
    lum: float


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://spiffy-blini-765515.netlify.app", "https://spiffy-blini-765515.netlify.app/"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/predict")
async def predict_anomaly(data_point: DataPoint):
    """
    Predice si un conjunto de condiciones ambientales (temperatura, humedad relativa, luminosidad) pertenecen al
    rango normal de valores o si se trata de una anomalía
    :return:
    """
    x = pd.DataFrame({
        'TEMPERATURA, °C': [data_point.temp],
        'HUMEDAD RELATIVA, %HR': [data_point.hum],
        'LUMINOSIDAD': [data_point.lum]
    })
    score = model.score_samples(x)
    anomaly = score < threshold
    return {
        "anomalia": anomaly.item(),
        "score": score.item()
    }
