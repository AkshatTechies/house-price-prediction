"""EstateIQ app shell and shared visual configuration."""
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
CSS_FILE = ROOT / "assets" / "style.css"


def apply_theme() -> None:
    """Load the design system once per page and render the persistent product identity."""
    with open(CSS_FILE, encoding="utf-8") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<div class='brand-lockup'><span class='brand-mark'>E</span><div><strong>EstateIQ</strong><small>Property intelligence</small></div></div>", unsafe_allow_html=True)
        st.caption("Valuation, location context, and comparable homes in one workspace.")


def section_title(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='hero'><span class='hero-tag'>ESTATEIQ</span><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)
