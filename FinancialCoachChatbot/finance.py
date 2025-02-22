def suggest_budget(income, expenses):
    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2
    if expenses > needs + wants:
        overspend = expenses - (needs + wants)
        coaching_tip = f"You’re overspending by ${overspend:.2f}. Cut back a little on wants—you’ve got this!"
    else:
        extra = (needs + wants) - expenses
        coaching_tip = f"Awesome—you’ve got ${extra:.2f} extra! Save it, and let’s build your future."
    return f"Budget: Needs (${needs:.2f}), Wants (${wants:.2f}), Savings (${savings:.2f}).\n{coaching_tip}"

def calculate_savings_growth(amount, months):
    monthly_rate = 0.04 / 12  # 4% annual interest
    future_value = amount * ((1 + monthly_rate) ** months)
    return f"Save ${amount:.2f} monthly for {months} months, and it could grow to ${future_value:.2f}. Imagine what you could do with that!"