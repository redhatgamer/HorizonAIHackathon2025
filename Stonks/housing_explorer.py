import streamlit as st

def calculate_mortgage(home_price, down_payment_percent, loan_term, interest_rate, property_tax_rate, insurance_cost):
    """Calculate monthly mortgage payment with Miami-specific costs."""
    down_payment = home_price * (down_payment_percent / 100)
    loan_amount = home_price - down_payment
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term * 12
    monthly_pi = (loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    monthly_tax = (home_price * (property_tax_rate / 100)) / 12
    monthly_insurance = insurance_cost / 12
    monthly_pmi = (0.005 * loan_amount) / 12 if down_payment_percent < 20 else 0  # PMI if down payment < 20%
    total_monthly = monthly_pi + monthly_tax + monthly_insurance + monthly_pmi
    return total_monthly, monthly_pi, monthly_tax, monthly_insurance, monthly_pmi

def display_housing_explorer():
    """Display the Miami Housing Affordability Explorer."""
    st.title("Miami Housing Affordability Explorer")
    st.markdown("""
        🏡 Navigate Miami’s wild housing market! Find out what you can afford, explore neighborhoods, 
        and plan for rising prices with Coach Stonks’ slick tool.
    """)

    # Inputs
    st.subheader("Your Financial Snapshot")
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Annual Income ($)", min_value=0, value=80000, step=1000)
        debt = st.number_input("Monthly Debt ($)", min_value=0, value=1000, step=100)
    with col2:
        down_payment_percent = st.slider("Down Payment (%)", 5, 50, 10)
        max_payment = st.number_input("Max Monthly Payment ($)", min_value=0, value=3500, step=100)

    # Miami-specific defaults
    st.subheader("Miami Market Settings")
    home_price = st.number_input("Target Home Price ($)", min_value=100000, value=550000, step=10000, help="Median Miami home price ~$550K")
    interest_rate = st.slider("Interest Rate (%)", 3.0, 10.0, 6.5)
    loan_term = st.selectbox("Loan Term (Years)", [15, 20, 30], index=2)
    property_tax_rate = 0.82  # Miami-Dade effective rate
    insurance_cost = 3500  # Annual, high due to hurricane risk

    # Calculate affordability
    total_monthly, pi, tax, ins, pmi = calculate_mortgage(home_price, down_payment_percent, loan_term, interest_rate, property_tax_rate, insurance_cost)
    affordable_price = (max_payment - (tax + ins + (pmi if down_payment_percent < 20 else 0))) * ((1 + interest_rate/1200) ** (loan_term*12) - 1) / ((interest_rate/1200) * (1 + interest_rate/1200) ** (loan_term*12)) * (1 - down_payment_percent/100)

    # Output
    st.subheader("Your Miami Home Breakdown")
    st.write(f"**Total Monthly Payment:** ${total_monthly:.2f}")
    st.write(f"- Principal & Interest: ${pi:.2f}")
    st.write(f"- Property Tax: ${tax:.2f}")
    st.write(f"- Insurance: ${ins:.2f}")
    if pmi > 0:
        st.write(f"- PMI: ${pmi:.2f}")
    st.write(f"**Max Affordable Price:** ${affordable_price:.2f} (based on your max payment)")

    # Neighborhood Visualizer
    st.subheader("Miami Neighborhoods")
    neighborhoods = {
        "Hialeah": 400000,
        "West Miami": 480000,
        "Miami Beach": 800000,
        "Coral Gables": 1200000
    }
    selected_neighborhood = st.selectbox("Explore Neighborhoods", list(neighborhoods.keys()))
    st.write(f"Median Price in {selected_neighborhood}: ${neighborhoods[selected_neighborhood]:,.0f}")
    if affordable_price >= neighborhoods[selected_neighborhood]:
        st.success(f"You can afford {selected_neighborhood}!")
    else:
        st.warning(f"{selected_neighborhood} is out of reach—save more or adjust your budget!")

    # Rising Price Buffer
    st.subheader("Plan for Rising Prices")
    years_to_buy = st.slider("Years Until Purchase", 1, 5, 2)
    appreciation_rate = 0.06  # 6% annual growth, Miami average
    future_price = home_price * (1 + appreciation_rate) ** years_to_buy
    extra_down_payment = (future_price * (down_payment_percent / 100)) - (home_price * (down_payment_percent / 100))
    monthly_savings = extra_down_payment / (years_to_buy * 12)
    st.write(f"In {years_to_buy} years, your ${home_price:,} home could cost ${future_price:,.0f}.")
    st.write(f"Save an extra ${monthly_savings:.2f}/month to keep up with the down payment.")