"""Property research assistant."""
import streamlit as st

from app.components.cards import section_heading
from app.components.theme import apply_theme
from utils.chatbot import chat

apply_theme()
section_heading("ASSISTANT", "Your property research companion", "Get practical guidance on comparing homes and understanding valuation inputs.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi — I can help you compare properties, review valuation inputs, and plan your purchase research."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about property research"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    response = chat(prompt, st.session_state.messages)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()
