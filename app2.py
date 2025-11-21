import os
import json
import streamlit as st
from groq import Groq

# Load API key from config.json
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

with open(config_path, "r") as f:
    config_data = json.load(f)

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit page config
st.set_page_config(
    page_title="Groq - ChatBot",
    page_icon="⚡",
    layout="centered"
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("⚡ Groq AI ChatBot ")

# Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Ask Groq...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Call Groq AI
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast & free Groq model
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            *st.session_state.chat_history
        ]
    )

    # Correct way to access Groq message content
    assistant_text = response.choices[0].message.content

    # Save and show assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
