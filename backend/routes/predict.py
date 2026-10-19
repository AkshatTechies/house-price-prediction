# backend/routes/predict.py
from fastapi import APIRouter, HTTPException
from backend.schemas import (
    HouseFeatures, PredictionResponse)
from utils.model_utils import model_metadata, model_performance, predict_price

router = APIRouter()

@router.post("/predict",
             response_model=PredictionResponse)
def predict(features: HouseFeatures):
    try:
        return PredictionResponse(predicted_price=predict_price(features.model_dump()))
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=503, detail="Prediction service is unavailable.") from exc


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "model": model_metadata()}


@router.get("/model-performance")
def get_model_performance() -> dict:
    return model_performance()
