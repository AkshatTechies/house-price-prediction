"""Resilient OpenStreetMap geocoding and amenity lookups."""
from __future__ import annotations

from functools import lru_cache

import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from utils.logging_config import get_logger

geolocator = Nominatim(user_agent="estateiq-location-intelligence/1.0", timeout=10)
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
logger = get_logger(__name__)


@lru_cache(maxsize=128)
def geocode_address(address: str) -> tuple[float | None, float | None]:
    """Convert a user supplied place to coordinates; failures are safe for the UI."""
    try:
        location = geolocator.geocode(address.strip(), exactly_one=True)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception:
        logger.exception("Geocoding failed")
        return None, None


@lru_cache(maxsize=512)
def get_nearby_places(lat: float, lng: float, place_type: str, radius: int = 2000) -> list[dict]:
    """Return named OSM nodes and ways around a location, sorted by straight-line distance."""
    osm_tags = {
        "school": ("amenity", "school"), "hospital": ("amenity", "hospital"),
        "restaurant": ("amenity", "restaurant"), "park": ("leisure", "park"),
        "gym": ("leisure", "fitness_centre"), "pharmacy": ("amenity", "pharmacy"),
        "bank": ("amenity", "bank"),
    }
    key, value = osm_tags[place_type]
    query = f'[out:json][timeout:20];(node["{key}"="{value}"](around:{radius},{lat},{lng});way["{key}"="{value}"](around:{radius},{lat},{lng}););out center;'
    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=25, headers={"User-Agent": "EstateIQ/1.0"})
        response.raise_for_status()
        places = []
        for element in response.json().get("elements", []):
            point = element.get("center", element)
            plat, plng = point.get("lat"), point.get("lon")
            if plat is None or plng is None:
                continue
            distance = geodesic((lat, lng), (plat, plng)).km
            places.append({
                "name": element.get("tags", {}).get("name", f"Unnamed {place_type}"),
                "lat": plat, "lng": plng, "distance_km": round(distance, 2), "type": place_type,
            })
        return sorted(places, key=lambda item: item["distance_km"])[:12]
    except requests.RequestException:
        logger.warning("Amenity lookup failed for %s", place_type, exc_info=True)
        return []


def calculate_distance_km(lat1, lng1, lat2, lng2):
    return round(geodesic((lat1, lng1), (lat2, lng2)).km, 2)
