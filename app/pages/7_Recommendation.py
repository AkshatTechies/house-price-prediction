import streamlit as st
from app.components.cards import property_card, section_heading
from app.components.theme import apply_theme
from utils.recommender import get_recommendations

apply_theme()
section_heading("COMPARABLES", "Find similar properties", "Describe your ideal home and compare the closest available matches.")
left, right = st.columns(2)
with left:
    area = st.slider("Target area (sq ft)", 300, 6000, 1200)
    bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5], index=1)
with right:
    bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
    loc_score = st.slider("Neighbourhood score", 0, 100, 60)
if st.button("Find comparable properties", type="primary"):
    results = get_recommendations({"area": area, "bedrooms": bedrooms, "bathrooms": bathrooms, "location_score": loc_score})
    st.markdown(f"### {len(results)} closest matches")
    for _, row in results.iterrows():
        property_card(row.to_dict())
