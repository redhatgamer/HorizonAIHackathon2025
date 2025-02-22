import streamlit as st
from chatbot import process_input
import stocks
import mortgage_calculator

st.set_page_config(page_title="Financial Coach Chatbot", layout="wide", initial_sidebar_state="collapsed")

# Load external CSS and JavaScript
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #1e1e1e;
            color: #f5f5f5;
        }

        .content-wrapper {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background: #2b2b2b;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .chat-message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
        }

        .coach-message {
            background-color: #3c3c3c;
            text-align: left;
            color: #00d4ff;
        }

        .user-message {
            background-color: #00d4ff;
            text-align: right;
            color: #1e1e1e;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #3c3c3c;
            color: #f5f5f5;
        }

        button {
            background-color: #00d4ff;
            color: #1e1e1e;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #00a3cc;
        }

        .stApp { 
            background-color: #1e1e1e; 
            color: #f5f5f5;
            font-family: 'Roboto', sans-serif;
            position: relative;
            min-height: 100vh;
            display: flex; /* Use flexbox for centering */
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            flex-direction: column; /* Stack items vertically */
            padding: 0; /* Remove default padding */
            margin: 0; /* Remove default margins */
        }

        .cube-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.5;
        }

        .cube {
            position: absolute;
            width: 50px;
            height: 50px;
            transform-style: preserve-3d;
            animation: rotate 20s infinite linear;
        }

        .cube div {
            position: absolute;
            width: 50px;
            height: 50px;
            background: rgba(0, 212, 255, 0.7);
            border: 1px solid rgba(0, 212, 255, 0.9);
        }

        .cube .front  { transform: translateZ(25px); }
        .cube .back   { transform: rotateY(180deg) translateZ(25px); }
        .cube .right  { transform: rotateY(90deg) translateZ(25px); }
        .cube .left   { transform: rotateY(-90deg) translateZ(25px); }
        .cube .top    { transform: rotateX(90deg) translateZ(25px); }
        .cube .bottom { transform: rotateX(-90deg) translateZ(25px); }

        @keyframes rotate {
            0% { transform: rotateX(0deg) rotateY(0deg); }
            100% { transform: rotateX(360deg) rotateY(360deg); }
        }

        .block {
            background: #2b2b2b;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
    </style>
    <div class="cube-container" id="cubeContainer"></div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const cubeContainer = document.getElementById("cubeContainer");
            // Add your cube animation logic here
        });
    </script>
""", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Menu")
menu_option = st.sidebar.selectbox("Choose an option", ["Home", "Stocks", "Mortgage Calculator"])

# Wrap content in a div to ensure it stays above the background
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

st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)