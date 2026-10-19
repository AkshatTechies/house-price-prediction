from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from utils.data_service import load_housing_data

df = load_housing_data()
FEATURES = ["area","bedrooms","bathrooms",
            "location_score"]
X = df[FEATURES].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

nn = NearestNeighbors(n_neighbors=6,
                      metric="cosine")
nn.fit(X_scaled)

def get_recommendations(user_prefs, n=5):
    """
    user_prefs: dict with area, bedrooms,
                bathrooms, location_score
    Returns top n similar properties as DataFrame.
    """
    import pandas as pd
    vec = scaler.transform(pd.DataFrame([{
        "area": user_prefs["area"],
        "bedrooms": user_prefs["bedrooms"],
        "bathrooms": user_prefs["bathrooms"],
        "location_score": user_prefs.get("location_score", 50),
    }]))
    n_neighbors = min(max(1, n), len(df))
    dists, idxs = nn.kneighbors(vec, n_neighbors=n_neighbors)

    matches = df.iloc[idxs[0]].copy()
    matches["match_pct"] = ((1 - dists[0]) * 100).clip(0, 100).round(1)
    return matches
