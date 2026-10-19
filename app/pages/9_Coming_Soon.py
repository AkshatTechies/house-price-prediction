"""Product roadmap page."""
import streamlit as st

from app.components.cards import feature_card, section_heading
from app.components.theme import apply_theme

apply_theme()
section_heading("ROADMAP", "What’s next for EstateIQ", "Focused product capabilities planned for future releases.")

features = [
    ("01", "Price forecasting", "See scenario-based local price movements over one to five years."),
    ("02", "Image analysis", "Review property photos for condition and renovation opportunities."),
    ("03", "Investment scoring", "Understand estimated yield, ROI, and investment fit."),
    ("04", "Safety analytics", "Explore area-level safety and neighbourhood indicators."),
]
grid = st.columns(2)
for index, feature in enumerate(features):
    with grid[index % 2]:
        feature_card(*feature)
st.info("Want a feature prioritised? Use the assistant to share what matters most to you.")
