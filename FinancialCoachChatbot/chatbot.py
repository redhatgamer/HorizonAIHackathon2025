# chatbot.py
import requests
import os  # For environment variables
from finance import suggest_budget, calculate_savings_growth

# Use environment variable for the API key (set in your system or Streamlit)
HF_API_KEY = os.getenv("HF_API_KEY", "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")  # Fallback for testing
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"  # Conversational model

def call_hf_api(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 200, "temperature": 0.7, "top_p": 0.95}
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["generated_text"].strip()
    except Exception as e:
        return f"Error with API: {e}"

def process_input(user_input, session_state):
    chat_history = session_state.get("chat_history", [])
    user_input = user_input.lower().strip()
    chat_history.append(("You", user_input))

    if user_input == "exit":
        chat_history.append(("Coach", "Catch you later—stay motivated!"))
        session_state["chat_history"] = chat_history
        session_state["exit"] = True
        return
    elif "i earn" in user_input or "my income is" in user_input:
        try:
            income = float(user_input.split("$")[-1].strip())
            session_state["waiting_for"] = "expenses"
            session_state["income"] = income
            session_state["budget_data"] = None  # Clear old budget data
            chat_history.append(("Coach", "How much do you spend monthly? Please enter a number like '$600'."))
        except ValueError:
            chat_history.append(("Coach", "Please use numbers, like 'I earn $500'."))
    elif "save" in user_input:
        session_state["waiting_for"] = "savings_amount"
        session_state["savings_data"] = None  # Clear old savings data
        chat_history.append(("Coach", "How much can you save monthly? Please enter a number like '$50'."))
    elif session_state.get("waiting_for") == "expenses":
        try:
            expenses = float(user_input.split("$")[-1].strip())
            budget = suggest_budget(session_state["income"], expenses)
            budget_data = get_budget_data(session_state["income"])
            session_state["budget_data"] = budget_data
            prompt = f"As a financial coach, respond to this user input with a helpful explanation and motivational nudge: The user’s budget is {budget}. What advice can you give?"
            response = call_hf_api(prompt)
            chat_history.append(("Coach", response))
            session_state["waiting_for"] = None
        except ValueError:
            chat_history.append(("Coach", "Please use a number, like '$600'."))
    elif session_state.get("waiting_for") == "savings_amount":
        try:
            amount = float(user_input.split("$")[-1].strip())
            session_state["waiting_for"] = "savings_months"
            session_state["savings_amount"] = amount
            chat_history.append(("Coach", "For how many months? Please enter a number like '12'."))
        except ValueError:
            chat_history.append(("Coach", "Please use a number, like '$50'."))
    elif session_state.get("waiting_for") == "savings_months":
        try:
            months = int(user_input)
            savings = calculate_savings_growth(session_state["savings_amount"], months)
            savings_data = get_savings_growth_data(session_state["savings_amount"], months)
            session_state["savings_data"] = savings_data
            prompt = f"As a financial coach, respond to this user input with a helpful explanation and motivational nudge: The user’s savings plan is {savings}. What advice can you give?"
            response = call_hf_api(prompt)
            chat_history.append(("Coach", response))
            session_state["waiting_for"] = None
        except ValueError:
            chat_history.append(("Coach", "Please enter a valid number, like '12'."))
    else:
        prompt = f"As a financial coach, respond to '{user_input}' with a helpful answer and a motivational nudge."
        response = call_hf_api(prompt)
        chat_history.append(("Coach", response))
    
    session_state["chat_history"] = chat_history