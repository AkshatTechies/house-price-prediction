"""EstateIQ application landing page."""
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.cards import feature_card
from app.components.footer import render_footer
from app.components.theme import apply_theme

st.set_page_config(page_title="EstateIQ | Property intelligence", page_icon="E", layout="wide", initial_sidebar_state="expanded")
apply_theme()

st.markdown("""<div class="hero"><span class="hero-tag">PROPERTY INTELLIGENCE</span>
<h1>Make your next move<br>with confidence.</h1><p>Estimate a home’s value, understand the market, and compare neighbourhoods in one calm, decision-ready workspace.</p></div>""", unsafe_allow_html=True)

metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Instant estimate", "< 1 sec", "Validated inputs")
metric_two.metric("Market signals", "6 cities", "Demo-ready")
metric_three.metric("Decision-ready", "₹ INR", "Transparent metrics")

left, right = st.columns([1.35, 1])
with left:
    st.markdown("### Start with the decision you need to make")
    st.write("Use the valuation model for a reliable first-pass estimate, then validate it against local pricing signals and nearby essentials.")
    if st.button("Estimate a property price", type="primary", use_container_width=True):
        st.switch_page("pages/2_Predict.py")
with right:
    st.markdown("<div class='insight-card'><span class='hero-tag'>HOW IT WORKS</span><h3>Inputs in. Context out.</h3><p>Area, layout, city, age, and location access are evaluated together by the selected valuation pipeline.</p></div>", unsafe_allow_html=True)

st.markdown("### Explore EstateIQ")
columns = st.columns(3)
for column, icon, title, description in zip(columns, ["01", "02", "03"], ["Estimate", "Understand", "Compare"], ["Generate a transparent price estimate.", "Explore pricing patterns and model quality.", "Find comparable homes and neighbourhood context."]):
    with column:
        feature_card(icon, title, description)
render_footer()
