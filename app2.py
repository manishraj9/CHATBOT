import os
import streamlit as st
from groq import Groq

# ✅ Load API key securely from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ✅ Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ✅ Streamlit page config
st.set_page_config(
    page_title="Groq - ChatBot",
    page_icon="⚡",
    layout="centered"
)

# ✅ Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("⚡ NovaChat AI – Groq-Powered Chatbot ")

# ✅ Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✅ User input
user_prompt = st.chat_input("Ask Groq...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # ✅ Call Groq AI
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            *st.session_state.chat_history
        ]
    )

    assistant_text = response.choices[0].message.content

    # ✅ Save and display assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
