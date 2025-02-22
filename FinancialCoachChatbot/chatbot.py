# chatbot.py
from finance import suggest_budget, calculate_savings_growth

# Response dictionary with nudges
responses = {
    "hi": "Hey there! I’m your Financial Coach—here to help you win with money. What’s on your mind?",
    "how do i budget": "Let’s craft a budget you’ll actually stick to! What’s your monthly income (e.g., 'I earn $500')?",
    "how do i save": "Saving’s your ticket to freedom! How much can you set aside each month?"
}

def process_input(user_input, session_state):
    """Process user input and update session state."""
    user_input = user_input.lower().strip()
    chat_history = session_state.get("chat_history", [])
    
    # Add user message
    chat_history.append(("You", user_input))

    if user_input == "exit":
        chat_history.append(("Coach", "Catch you later—stay motivated!"))
        session_state["chat_history"] = chat_history
        session_state["exit"] = True
        return
    elif user_input in responses:
        chat_history.append(("Coach", responses[user_input]))
    elif "i earn" in user_input or "my income is" in user_input:
        try:
            income = float(user_input.split("$")[-1].strip())
            session_state["waiting_for"] = "expenses"
            session_state["income"] = income
            chat_history.append(("Coach", "How much do you spend monthly? Type a number like '$600'."))
        except ValueError:
            chat_history.append(("Coach", "Please use numbers, like 'I earn $500'."))
    elif "save" in user_input:
        session_state["waiting_for"] = "savings_amount"
        chat_history.append(("Coach", "How much can you save monthly? Type a number like '$50'."))
    elif session_state.get("waiting_for") == "expenses":
        try:
            expenses = float(user_input.split("$")[-1].strip())
            budget = suggest_budget(session_state["income"], expenses)
            chat_history.append(("Coach", budget))
            session_state["waiting_for"] = None
        except ValueError:
            chat_history.append(("Coach", "Please use a number, like '$600'."))
    elif session_state.get("waiting_for") == "savings_amount":
        try:
            amount = float(user_input.split("$")[-1].strip())
            session_state["waiting_for"] = "savings_months"
            session_state["savings_amount"] = amount
            chat_history.append(("Coach", "For how many months? Type a number like '12'."))
        except ValueError:
            chat_history.append(("Coach", "Please use a number, like '$50'."))
    elif session_state.get("waiting_for") == "savings_months":
        try:
            months = int(user_input)
            savings = calculate_savings_growth(session_state["savings_amount"], months)
            chat_history.append(("Coach", savings))
            session_state["waiting_for"] = None
        except ValueError:
            chat_history.append(("Coach", "Please enter a valid number, like '12'."))
    else:
        chat_history.append(("Coach", "Hmm, let’s try that again. Ask about budgeting or saving!"))
    
    session_state["chat_history"] = chat_history