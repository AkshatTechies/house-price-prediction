"""Safe, offline first assistant for general real-estate guidance."""
from __future__ import annotations

def chat(prompt: str, history: list[dict] | None = None) -> str:
    text = prompt.lower()
    if any(word in text for word in ("price", "cost", "value", "estimate")):
        return "For a personalised estimate, open Predict and enter the home’s area, layout, city, age, and neighbourhood score. Treat the result as an indicative range and compare recent local sales before acting."
    if any(word in text for word in ("buy", "purchase", "check")):
        return "Before buying, verify ownership and approvals, inspect the building condition, compare recent transactions nearby, and budget for registration, maintenance, and financing costs. A qualified local professional can verify legal and valuation details."
    if any(word in text for word in ("location", "area", "neighbourhood")):
        return "A strong neighbourhood review considers commute time, schools and healthcare, flood risk, planned infrastructure, safety, and recent transaction prices. The Map page can help you explore nearby amenities."
    return "I can help you plan a property search, understand valuation inputs, or compare neighbourhood factors. What would you like to explore?"
