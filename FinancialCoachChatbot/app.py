# app.py
import streamlit as st
from chatbot import process_input
import plotly.graph_objs as go

st.set_page_config(page_title="Financial Coach Chatbot", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #2B2B2B; color: #FFFFFF; }
    .stTextInput > div > div > input { background-color: #4A4A4A; color: #FFFFFF; border-radius: 10px; padding: 10px; }
    .stButton > button { background-color: #00D4FF; color: #FFFFFF; border-radius: 10px; padding: 10px 20px; font-weight: bold; }
    .stButton > button:hover { background-color: #00A3CC; }
    </style>
""", unsafe_allow_html=True)

st.title("Financial Coach Chatbot")
st.markdown("Your modern money mentor—budget, save, and thrive!")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [("Coach", "Welcome! I’m here to help you with money. Ask away!")]
if "exit" not in st.session_state:
    st.session_state["exit"] = False

# Chat display
chat_container = st.container()
with chat_container:
    for sender, message in st.session_state["chat_history"]:
        st.markdown(f"**{sender}:** {message}", unsafe_allow_html=True)

# Display graphs if data exists
if "budget_data" in st.session_state and st.session_state["budget_data"]:
    budget_data = st.session_state["budget_data"]
    fig_budget = go.Figure(data=[go.Pie(labels=budget_data["labels"], values=budget_data["values"], hole=0.3)])
    fig_budget.update_layout(
        plot_bgcolor="#2B2B2B",
        paper_bgcolor="#2B2B2B",
        font_color="#FFFFFF",
        title_text="Your Budget Breakdown (50/30/20)",
        title_font_color="#00D4FF"
    )
    st.plotly_chart(fig_budget, use_container_width=True)

if "savings_data" in st.session_state and st.session_state["savings_data"]:
    savings_data = st.session_state["savings_data"]
    fig_savings = go.Figure(data=[go.Scatter(x=savings_data["months"], y=savings_data["values"], mode='lines+markers', name='Savings Growth')])
    fig_savings.update_layout(
        plot_bgcolor="#2B2B2B",
        paper_bgcolor="#2B2B2B",
        font_color="#FFFFFF",
        title_text="Your Savings Growth Over Time",
        title_font_color="#00D4FF",
        xaxis_title="Months",
        yaxis_title="Value ($)"
    )
    st.plotly_chart(fig_savings, use_container_width=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me something:", placeholder="e.g., 'I earn $500' or 'How do I save?'")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    process_input(user_input, st.session_state)
    if st.session_state["exit"]:
        st.stop()
    st.rerun()

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)