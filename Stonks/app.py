import streamlit as st
from chatbot import process_input
import stocks
import mortgage_calculator

# Set page configuration
st.set_page_config(page_title="Financial Coach Chatbot", layout="wide", initial_sidebar_state="collapsed")

# Load external CSS
with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load external JavaScript
with open("static/scripts.js") as f:
    st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Menu")
menu_option = st.sidebar.selectbox("Choose an option", ["Home", "Stocks", "Mortgage Calculator"])

# Content wrapper
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

if menu_option == "Home":
    st.title("Stonks")
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
            if sender == "Coach":
                st.markdown(f'<div class="chat-message coach-message">{sender}: {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message user-message">{sender}: {message}</div>', unsafe_allow_html=True)

    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask me something:", placeholder="e.g., 'I earn $500' or 'How do I save?'")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        process_input(user_input, st.session_state)
        if st.session_state["exit"]:
            st.stop()
        st.rerun()

elif menu_option == "Stocks":
    stocks.display_stocks()

elif menu_option == "Mortgage Calculator":
    mortgage_calculator.display_mortgage_calculator()

# Close content wrapper and add scroll script
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)