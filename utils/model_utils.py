"""Model training, selection, and inference for EstateIQ."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from utils.data_service import load_housing_data

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "best_model.joblib"
METADATA_PATH = ROOT / "models" / "model_metrics.json"
FEATURES = ["area", "bedrooms", "bathrooms", "location", "age_years", "location_score"]


def _preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [("location", OneHotEncoder(handle_unknown="ignore"), ["location"])],
        remainder="passthrough",
    )


def _candidates() -> dict[str, object]:
    return {
        "Random Forest": RandomForestRegressor(
            n_estimators=350, min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=350, min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
    }


def build_pipeline(model: object | None = None) -> Pipeline:
    """Build the selected production pipeline (Extra Trees by default)."""
    estimator = model if model is not None else _candidates()["Extra Trees"]
    return Pipeline([("preprocessor", _preprocessor()), ("model", estimator)])


def train_and_save_model() -> Pipeline:
    """Compare candidate models on a held-out set, then fit the winner on all data."""
    data = load_housing_data()

    missing_cols = set(FEATURES + ["price"]) - set(data.columns)
    if missing_cols:
        raise ValueError(f"Housing data missing required columns: {sorted(missing_cols)}")
    if len(data) < 10:
        raise ValueError("Not enough rows to train/test split reliably.")

    train, test = train_test_split(data, test_size=0.20, random_state=42)
    results: dict[str, dict[str, float]] = {}

    for name, estimator in _candidates().items():
        pipeline = build_pipeline(estimator)
        pipeline.fit(train[FEATURES], train["price"])
        prediction = pipeline.predict(test[FEATURES])
        results[name] = {
            "r2": round(float(r2_score(test["price"], prediction)), 4),
            "mae": round(float(mean_absolute_error(test["price"], prediction)), 2),
            "rmse": round(float(mean_squared_error(test["price"], prediction) ** 0.5), 2),
        }

    # R² is the primary quality signal; MAE resolves near ties in favour of lower error.
    winner = max(results, key=lambda name: (results[name]["r2"], -results[name]["mae"]))
    model = build_pipeline(_candidates()[winner])
    model.fit(data[FEATURES], data["price"])

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    METADATA_PATH.write_text(
        json.dumps(
            {
                "selected_model": winner,
                "selection_rule": "Highest hold-out R²; lower MAE breaks ties.",
                "test_split": 0.20,
                "rows": len(data),
                "features": FEATURES,
                "metrics": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    load_model.cache_clear()
    return model


@lru_cache(maxsize=1)
def load_model() -> Pipeline:
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        return train_and_save_model()
    return joblib.load(MODEL_PATH)


def predict_price(features: dict) -> float:
    missing = set(FEATURES) - set(features)
    if missing:
        raise ValueError(f"Missing prediction fields: {', '.join(sorted(missing))}")
    values = pd.DataFrame([{column: features[column] for column in FEATURES}])
    prediction = load_model().predict(values)[0]
    return round(float(prediction), 2)


def model_performance() -> dict:
    """Return a persisted, UI-safe explanation of the currently selected model."""
    load_model()
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def model_metadata() -> dict:
    performance = model_performance()
    return {
        "features": FEATURES,
        "artifact": str(MODEL_PATH),
        "trained": MODEL_PATH.exists(),
        "selected_model": performance["selected_model"],
    }