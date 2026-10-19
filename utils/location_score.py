# utils/location_score.py
from utils.maps import get_nearby_places

def calculate_location_score(lat, lng, radius=2000, places_by_type=None):
    """Score a location from 0 to 100."""
    categories = {
        "school":     {"weight": 25, "ideal": 3},
        "hospital":   {"weight": 25, "ideal": 2},
        "restaurant": {"weight": 20, "ideal": 5},
        "park":       {"weight": 15, "ideal": 2},
        "pharmacy":   {"weight": 15, "ideal": 2},
    }
    breakdown = {}
    total = 0.0

    for ptype, cfg in categories.items():
        places = (places_by_type or {}).get(ptype)
        if places is None:
            places = get_nearby_places(lat, lng, ptype, radius)
        count = len(places)
        ratio = min(count / cfg["ideal"], 1.0)
        score = round(ratio * cfg["weight"], 1)
        breakdown[ptype] = {
            "found": count,
            "score": score,
            "max":   cfg["weight"],
            "places": places
        }
        total += score

    return round(total, 1), breakdown
