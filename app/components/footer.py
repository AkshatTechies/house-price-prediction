import streamlit as st


def render_footer() -> None:
    st.markdown(
        '<div class="app-footer">Real Estate AI · Estimates are decision-support signals, not formal valuations.</div>',
        unsafe_allow_html=True,
    )
