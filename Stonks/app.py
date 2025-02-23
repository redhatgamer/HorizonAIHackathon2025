import streamlit as st
from chatbot import process_input
import stocks
import mortgage_calculator
import housing_explorer  # New module for the housing tool
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration with enhanced branding
st.set_page_config(
    page_title="Stonks - Your Financial Ally",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load external CSS with error handling
try:
    with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error("CSS file not found. Using default styling.")
    st.markdown("""
        <style>
            .content-wrapper { padding: 20px; }
            .chat-message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .coach-message { background-color: #e6f3ff; }
            .user-message { background-color: #f0f0f0; text-align: right; }
            .sidebar .sidebar-content { background-color: #f8f9fa; }
        </style>
    """, unsafe_allow_html=True)

# Load external JavaScript with error handling
try:
    with open("static/scripts.js") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error("JavaScript file not found. Basic functionality will still work.")

# Sidebar menu with enhanced styling and options
with st.sidebar:
    st.title("💸 Stonks Dashboard")
    st.markdown("Navigate your financial journey:")
    menu_option = st.selectbox(
        "Choose Your Path",
        ["Home", "Stocks", "Mortgage Calculator", "Housing Explorer"],
        help="Pick a tool to boost your financial game!"
    )
    st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")

# Content wrapper for consistent layout
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Home Section - Chatbot Interface
if menu_option == "Home":
    st.title("Welcome to Stonks!")
    st.markdown("""
        Your modern money mentor—budget, save, and thrive with Coach Stonks by your side!
    """)

    # Avatar and introduction
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(
            "https://i.pinimg.com/474x/bc/a6/f0/bca6f050d4be2e7e045041400679cc9a.jpg",
            width=100,
            caption="Coach Stonks"
        )
    with col2:
        st.markdown("""
            Meet **Coach Stonks**, your financial hype-man! Whether you're stacking cash, 
            plotting investments, or dodging money traps, I’ve got your back. Let’s talk!
        """)

    # Session state initialization
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            ("Coach Stonks", "Yo, money maestro! I’m Coach Stonks, your financial wingman. What’s the vibe—cash flow woes, investment dreams, or just tired of overpriced lattes?")
        ]
    if "exit" not in st.session_state:
        st.session_state["exit"] = False
    if "last_interaction" not in st.session_state:
        st.session_state["last_interaction"] = datetime.now()

    # Option to enlarge chat
    enlarge_chat = st.checkbox("Enlarge Chat", value=False)
    chat_height = "600px" if enlarge_chat else "400px"

    # Chat display with a scrollable container
    chat_container_html = f'<div style="height: {chat_height}; overflow-y: auto; padding-right: 10px;">'
    for sender, message in st.session_state["chat_history"]:
        if sender == "Coach Stonks":
            chat_container_html += (
                f'<div class="chat-message coach-message">'
                f'<b>{sender}:</b> {message}'
                f'</div>'
            )
        else:
            chat_container_html += (
                f'<div class="chat-message user-message">'
                f'<b>{sender}:</b> {message}'
                f'</div>'
            )
    chat_container_html += '</div>'
    st.markdown(chat_container_html, unsafe_allow_html=True)

    # Input form with validation and placeholder examples
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Talk to Coach Stonks:",
            placeholder="Try 'I earn $500/week', 'How do I invest?', or 'Help me budget!'",
            help="Ask anything money-related!"
        )
        col_submit, col_clear = st.columns([1, 1])
        with col_submit:
            submit_button = st.form_submit_button(label="Send 🚀")
        with col_clear:
            clear_button = st.form_submit_button(label="Clear Chat")

    # Process input
    if submit_button and user_input.strip():
        try:
            process_input(user_input, st.session_state)
            st.session_state["last_interaction"] = datetime.now()
            if st.session_state["exit"]:
                st.success("Thanks for chatting! Catch you later!")
                st.stop()
            st.rerun()
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
            logger.error(f"Error processing input: {e}")

    # Clear chat history
    if clear_button:
        st.session_state["chat_history"] = [
            ("Coach Stonks", "Chat reset! What’s up now, fam?")
        ]
        st.rerun()

# Stocks Section
elif menu_option == "Stocks":
    try:
        stocks.display_stocks()
    except Exception as e:
        st.error("Couldn’t load the stock tools. Try again later!")
        logger.error(f"Stocks module error: {e}")

# Mortgage Calculator Section
elif menu_option == "Mortgage Calculator":
    try:
        mortgage_calculator.display_mortgage_calculator()
    except Exception as e:
        st.error("Mortgage calculator hit a snag. Check back soon!")
        logger.error(f"Mortgage calculator error: {e}")

# Housing Explorer Section
elif menu_option == "Housing Explorer":
    try:
        housing_explorer.display_housing_explorer()
    except Exception as e:
        st.error("Housing Explorer hit a glitch. Try again soon!")
        logger.error(f"Housing Explorer error: {e}")

# Footer and cleanup
st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        Powered by Stonks © 2025 | Built with 💪 by xAI
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll to bottom of chat
st.markdown("""
    <script>
        let chatContainer = document.querySelector('.stContainer');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
""", unsafe_allow_html=True)