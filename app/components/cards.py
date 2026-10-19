"""Small reusable presentation components for EstateIQ."""
import streamlit as st


def section_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="section-header"><h2>{title}</h2><p>{subtitle}</p></div>', unsafe_allow_html=True)


def section_heading(eyebrow: str, title: str, subtitle: str = ""):
    st.markdown(f'<div class="hero"><span class="hero-tag">{eyebrow}</span><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def kpi_card(title: str, value: str, icon: str = "📊", delta: str | None = None):
    delta_html = f'<p class="kpi-change">{delta}</p>' if delta else ""
    st.markdown(f'<div class="kpi-card"><div class="kpi-header"><span>{title}</span><span>{icon}</span></div><h2>{value}</h2>{delta_html}</div>', unsafe_allow_html=True)


def feature_card(icon: str, title: str, description: str):
    st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{description}</p></div>', unsafe_allow_html=True)


def property_card(property_data: dict):
    st.markdown(
        f'''<div class="property-card"><h3>{property_data.get("location", "Comparable property")}</h3>
        <p>Location score: {property_data.get("location_score", "—")}/100</p>
        <h2>₹{property_data.get("price", 0):,.0f}</h2>
        <div class="property-meta"><span>🛏 {property_data.get("bedrooms", "—")} beds</span>
        <span>🛁 {property_data.get("bathrooms", "—")} baths</span>
        <span>📐 {property_data.get("area", "—"):,} sq ft</span></div></div>''', unsafe_allow_html=True)


def stat_card(value: str, label: str):
    st.markdown(f'<div class="stat-card"><h2>{value}</h2><p>{label}</p></div>', unsafe_allow_html=True)


def empty_state(title: str = "No Data Found", message: str = "Try changing your search filters."):
    st.info(f"{title}: {message}")


def loading_skeleton(message: str = "Loading..."):
    return st.spinner(message)
