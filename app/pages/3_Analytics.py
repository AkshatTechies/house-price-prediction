import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app.components.cards import section_heading
from app.components.theme import apply_theme
from utils.data_service import load_housing_data
from utils.model_utils import model_performance

@st.cache_data(show_spinner=False)
def get_data():
    return load_housing_data()

apply_theme()
data = get_data()
section_heading("MARKET PULSE", "Understand local price signals", "Interactive views of the available property dataset.")
with st.sidebar:
    st.markdown("### Filters")
    price_range = st.slider("Price range (₹)", int(data.price.min()), int(data.price.max()), (int(data.price.min()), int(data.price.max())))
    locations = st.multiselect("Cities", sorted(data.location.unique()), default=sorted(data.location.unique()))
    beds = st.multiselect("Bedrooms", sorted(data.bedrooms.unique()), default=sorted(data.bedrooms.unique()))
filtered = data[data.price.between(*price_range) & data.location.isin(locations) & data.bedrooms.isin(beds)]
if filtered.empty:
    st.warning("No properties match these filters. Adjust the filters to continue.")
    st.stop()
a,b,c = st.columns(3)
a.metric("Properties", f"{len(filtered):,}")
b.metric("Median price", f"₹{filtered.price.median()/1e6:.1f}M")
c.metric("Median price / sq ft", f"₹{(filtered.price/filtered.area).median():,.0f}")
st.markdown("### Valuation model performance")
performance = model_performance()
winner = performance["selected_model"]
winner_metrics = performance["metrics"][winner]
metric_left, metric_middle, metric_right = st.columns(3)
metric_left.metric("Selected model", winner)
metric_middle.metric("Hold-out R²", f"{winner_metrics['r2']:.1%}", help="Share of price variation explained on unseen test data.")
metric_right.metric("Typical error (MAE)", f"₹{winner_metrics['mae']:,.0f}", help="Average absolute difference between predicted and observed price.")
st.caption(f"Selection: {performance['selection_rule']} Evaluated on {performance['rows']} rows with a fixed {int(performance['test_split'] * 100)}% hold-out test set.")
comparison = [{"Model": name, "R²": values["r2"], "MAE (₹)": values["mae"], "RMSE (₹)": values["rmse"], "Selected": "Yes" if name == winner else ""} for name, values in performance["metrics"].items()]
st.dataframe(comparison, hide_index=True, use_container_width=True, column_config={"R²": st.column_config.NumberColumn(format="%.1%"), "MAE (₹)": st.column_config.NumberColumn(format="₹%.0f"), "RMSE (₹)": st.column_config.NumberColumn(format="₹%.0f")})
with st.expander("How the model works"):
    st.markdown("**Extra Trees / Random Forest** are tree ensembles: they learn non-linear relationships between size, layout, city, age and neighbourhood score without assuming a straight-line price curve. City is one-hot encoded, both candidates are trained on the same 80% sample, and the winner is refit on all available data after evaluation. R² measures explanatory power; MAE and RMSE report error in rupees. This is a decision-support estimate—not an appraisal.")

left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="area", y="price", color="location", size="bedrooms", hover_data=["bathrooms", "age_years", "location_score"], labels={"area":"Area (sq ft)","price":"Price (₹)","location":"City"}, template="plotly_dark")
    fig.update_layout(title="Area and price", height=410, legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_location = filtered.groupby("location", as_index=False).price.mean().sort_values("price")
    fig = px.bar(by_location, x="price", y="location", orientation="h", color="price", color_continuous_scale=["#36506d", "#55d6be"], labels={"price":"Average price (₹)","location":""}, template="plotly_dark")
    fig.update_layout(title="Average price by city", height=410, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
st.markdown("### Distribution and drivers")
left, right = st.columns(2)
with left:
    fig = px.histogram(filtered, x="price", nbins=28, color_discrete_sequence=["#55d6be"], labels={"price":"Price (₹)"}, template="plotly_dark")
    fig.update_layout(title="Price distribution", height=350)
    st.plotly_chart(fig, use_container_width=True)
with right:
    corr = filtered.select_dtypes("number").corr().round(2)
    fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale="Tealrose", zmid=0, text=corr.values, texttemplate="%{text}"))
    fig.update_layout(title="Feature correlation", height=350, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
