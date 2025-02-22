# app.py
import streamlit as st
from chatbot import process_input

# Configure page
st.set_page_config(page_title="Financial Coach Chatbot", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp {
        background-color: #2B2B2B;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #4A4A4A;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #00D4FF;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #00A3CC;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Financial Coach Chatbot")
st.markdown("Your modern money mentor—budget, save, and thrive!")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Coach", "Welcome! I’m here to help you with money. Ask away!")]
if "exit" not in st.session_state:
    st.session_state["exit"] = False

# Chat display
chat_container = st.container()
with chat_container:
    for sender, message in st.session_state["chat_history"]:
        if sender == "You":
            st.markdown(f"**{sender}:** {message}", unsafe_allow_html=True)
        else:
            st.markdown(f"**{sender}:** {message}", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me something:", placeholder="e.g., 'I earn $500' or 'How do I save?'")
    submit_button = st.form_submit_button(label="Send")

# Process input
if submit_button and user_input:
    process_input(user_input, st.session_state)
    if st.session_state["exit"]:
        st.stop()  # Stops the app on "exit"
    st.rerun()  # Refresh to update chat

# Scroll to bottom (hacky but works)
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)