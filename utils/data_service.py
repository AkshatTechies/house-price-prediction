"""Dataset loading and deterministic demo-data support."""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "housing.csv"
REQUIRED_COLUMNS = {"area", "bedrooms", "bathrooms", "location", "age_years", "location_score", "price"}


def _demo_data(rows: int = 360) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    locations = {"Bangalore": 1.18, "Mumbai": 1.65, "Delhi": 1.32, "Pune": 0.92, "Hyderabad": 0.84, "Chennai": 0.88}
    location = rng.choice(list(locations), rows)
    area = rng.integers(450, 4200, rows)
    bedrooms = np.clip(np.rint(area / 800 + rng.normal(0, .65, rows)), 1, 5).astype(int)
    bathrooms = np.clip(bedrooms + rng.integers(-1, 2, rows), 1, 5)
    age_years = rng.integers(0, 32, rows)
    location_score = rng.integers(38, 98, rows)
    multiplier = np.array([locations[item] for item in location])
    price = (area * 7800 * multiplier + bedrooms * 500_000 + location_score * 22_000 - age_years * 75_000 + rng.normal(0, 750_000, rows)).clip(2_500_000)
    return pd.DataFrame({"area": area, "bedrooms": bedrooms, "bathrooms": bathrooms, "location": location, "age_years": age_years, "location_score": location_score, "price": price.round(0)})


@lru_cache(maxsize=1)
def _load_housing_data() -> pd.DataFrame:
    """Load project data, falling back to a clearly marked deterministic demo set."""
    if DATA_PATH.exists():
        dataframe = pd.read_csv(DATA_PATH)
        missing = REQUIRED_COLUMNS - set(dataframe.columns)
        if missing:
            raise ValueError(f"housing.csv is missing required columns: {', '.join(sorted(missing))}")
        return dataframe
    return _demo_data()


def load_housing_data() -> pd.DataFrame:
    """Return an isolated copy so page filters never mutate cached source data."""
    return _load_housing_data().copy()
