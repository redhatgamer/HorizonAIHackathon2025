import streamlit as st
import finnhub
import os
from datetime import datetime, timedelta

# Initialize Finnhub client with API key from environment variable
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY", "cut1topr01qrsirk847gcut1topr01qrsirk8480"))

def fetch_stock_quote(symbol):
    """Fetch and return the current stock quote for a given symbol."""
    try:
        return finnhub_client.quote(symbol.upper())
    except Exception as e:
        st.error(f"Error fetching stock price for {symbol}: {e}")
        return None

def fetch_company_profile(symbol):
    """Fetch and return the company profile for a given symbol."""
    try:
        return finnhub_client.company_profile2(symbol=symbol.upper())
    except Exception as e:
        st.error(f"Error fetching company profile for {symbol}: {e}")
        return None

def fetch_company_news(symbol, days_back=365):
    """Fetch recent news articles for a given symbol."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    try:
        return finnhub_client.company_news(
            symbol.upper(), 
            _from=start_date.strftime("%Y-%m-%d"), 
            to=end_date.strftime("%Y-%m-%d")
        )
    except Exception as e:
        st.error(f"Error fetching news for {symbol}: {e}")
        return []

def calculate_investment(symbol, amount, stock_price):
    """Calculate the number of shares that can be bought with a given investment amount."""
    if stock_price and stock_price['c'] > 0:
        shares = amount / stock_price['c']
        return f"With ${amount:,.2f}, you can buy approximately {shares:.2f} shares of {symbol.upper()} at ${stock_price['c']:,.2f} per share."
    return "Unable to calculate shares due to missing price data."

def display_stock_dashboard(symbol, investment_amount):
    """Display a comprehensive stock dashboard for a given symbol."""
    st.subheader(f"Stock Dashboard: {symbol.upper()}")

    # Fetch and display stock quote
    stock_price = fetch_stock_quote(symbol)
    if stock_price:
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${stock_price['c']:,.2f}")
        col2.metric("High Price", f"${stock_price['h']:,.2f}")
        col3.metric("Low Price", f"${stock_price['l']:,.2f}")
        col1.metric("Open Price", f"${stock_price['o']:,.2f}")
        col2.metric("Previous Close", f"${stock_price['pc']:,.2f}")
        col3.metric("Change", f"{((stock_price['c'] - stock_price['pc']) / stock_price['pc'] * 100):.2f}%")

    # Fetch and display company profile
    company_profile = fetch_company_profile(symbol)
    if company_profile:
        st.subheader("Company Profile")
        st.markdown(f"""
            **Name:** {company_profile.get('name', 'N/A')}  
            **Industry:** {company_profile.get('finnhubIndustry', 'N/A')}  
            **Market Cap:** ${company_profile.get('marketCapitalization', 'N/A'):,.2f}B  
            **Shares Outstanding:** {company_profile.get('shareOutstanding', 'N/A'):,.2f}M  
            **Website:** [{company_profile.get('weburl', 'N/A')}]({company_profile.get('weburl', 'N/A')})
        """)

    # Investment Calculator
    if investment_amount > 0 and stock_price:
        st.subheader("Investment Calculator")
        st.write(calculate_investment(symbol, investment_amount, stock_price))

    # Fetch and display news
    news = fetch_company_news(symbol)
    if news:
        st.subheader("Latest News")
        for article in news[:5]:
            st.markdown(f"""
                **{article.get('headline', 'No Title')}**  
                {article.get('summary', 'No Summary')}  
                [Read more]({article.get('url', '#')})  
                ---
            """)

def display_stocks():
    """Main function to render the stocks page."""
    st.title("Stock Portfolio Analyzer")
    st.markdown("Track stock prices, analyze companies, and calculate investments.")

    # Load custom CSS
    with open("styles/stocks.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Stock symbol input
    stock_symbol = st.text_input("Enter stock symbol:", placeholder="e.g., AAPL, TSLA", key="stock_symbol").strip()
    
    # Investment amount input
    investment_amount = st.number_input("Investment Amount (USD):", min_value=0.0, step=100.0, value=0.0, key="investment_amount")

    # Portfolio tracking feature
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}

    if st.button("Add to Portfolio") and stock_symbol:
        stock_price = fetch_stock_quote(stock_symbol)
        if stock_price:
            st.session_state.portfolio[stock_symbol.upper()] = {
                "price": stock_price['c'],
                "shares": investment_amount / stock_price['c'] if investment_amount > 0 else 0
            }
            st.success(f"{stock_symbol.upper()} added to portfolio!")

    # Display portfolio
    if st.session_state.portfolio:
        st.subheader("Your Portfolio")
        total_value = 0
        for symbol, data in st.session_state.portfolio.items():
            current_price = fetch_stock_quote(symbol)['c']
            value = current_price * data['shares']
            total_value += value
            st.write(f"{symbol}: {data['shares']:.2f} shares @ ${current_price:,.2f} = ${value:,.2f}")
        st.write(f"**Total Portfolio Value:** ${total_value:,.2f}")

    # Display stock dashboard if a symbol is entered
    if stock_symbol:
        display_stock_dashboard(stock_symbol, investment_amount)