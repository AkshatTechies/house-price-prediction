import streamlit as st
import plotly.graph_objects as go
from app.components.cards import section_heading
from app.components.theme import apply_theme
from utils.data_service import load_housing_data
from utils.model_utils import predict_price

apply_theme()
section_heading("VALUATION", "Estimate a property price", "Provide a few reliable details. The estimate is a planning signal, not a formal appraisal.")
data = load_housing_data()
with st.form("prediction_form", border=False):
    left, right = st.columns(2)
    with left:
        area = st.number_input("Built-up area (sq ft)", min_value=200, max_value=100_000, value=1200, step=50)
        bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5], index=1)
        bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
    with right:
        location = st.selectbox("City", sorted(data["location"].unique()))
        age = st.slider("Property age (years)", 0, 80, 5)
        loc_score = st.slider("Neighbourhood score", 0, 100, 65, help="Use Map to assess nearby amenities.")
    submitted = st.form_submit_button("Generate estimate", type="primary", use_container_width=True)
if submitted:
    payload = {"area": area, "bedrooms": bedrooms, "bathrooms": bathrooms, "location": location, "age_years": age, "location_score": loc_score}
    try:
        st.session_state["last_prediction"] = {**payload, "price": predict_price(payload)}
    except (ValueError, OSError):
        st.error("We could not generate an estimate. Check the supplied property details and try again.")
result = st.session_state.get("last_prediction")
if result:
    estimate = result["price"]
    low, high = estimate * .90, estimate * 1.10
    st.markdown("### Your indicative valuation")
    a, b, c = st.columns(3)
    a.metric("Estimated value", f"₹{estimate:,.0f}")
    b.metric("Expected range", f"₹{low/1e6:.1f}M–₹{high/1e6:.1f}M")
    c.metric("Price per sq ft", f"₹{estimate/result['area']:,.0f}")
    fig = go.Figure(go.Indicator(mode="gauge+number", value=result["location_score"], number={"suffix": "/100"}, title={"text": "Neighbourhood signal"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#55d6be"}, "steps": [{"range": [0, 50], "color": "#27314a"}, {"range": [50, 75], "color": "#36506d"}]}))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=0), paper_bgcolor="rgba(0,0,0,0)", font_color="#eef3ff")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The range reflects normal model uncertainty. Verify title, condition, micro-location, and current comparable sales before making financial decisions.")
