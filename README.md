# Real Estate AI

An end-to-end house-price intelligence app with a Streamlit dashboard and FastAPI prediction service.

## Run locally

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

In another terminal:

```powershell
.\venv\Scripts\streamlit.exe run app/main.py
```

The API is available at `http://localhost:8000/docs`. Submit predictions to `POST /api/v1/predict`, check it with `GET /api/v1/health`, and retrieve the selected model's evaluation report at `GET /api/v1/model-performance`.

## Data and model

Place real data at `data/housing.csv` using these columns:

`area, bedrooms, bathrooms, location, age_years, location_score, price`

If the file is absent, the app uses deterministic demo data so every page remains usable. Train or retrain the model with:

```powershell
.\venv\Scripts\python.exe models/train.py
```

The generated model is stored in `models/best_model.joblib` and is intentionally excluded from source control in production.

Training compares Random Forest and Extra Trees on a fixed 20% hold-out set. The model with the highest R² (then lowest MAE for ties) is selected, refit on all data, and its R², MAE, and RMSE are persisted to `models/model_metrics.json`. The Analytics page presents that report in plain language.

## Location intelligence

The Map page geocodes an address through OpenStreetMap and dynamically loads nearby amenities from Overpass. Search results persist while navigating the page, render as clustered markers, and contribute to a transparent amenity score. Network availability and third-party coverage affect live map results.
