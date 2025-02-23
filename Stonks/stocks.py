import streamlit as st
import finnhub
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go

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

def fetch_historical_data(symbol, start_date, end_date):
    """Fetch historical stock price data for a given symbol."""
    try:
        return finnhub_client.stock_candles(symbol.upper(), 'D', int(start_date.timestamp()), int(end_date.timestamp()))
    except Exception as e:
        st.error(f"Error fetching historical data for {symbol}: {e}")
        return None

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
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                **Name:** {company_profile.get('name', 'N/A')}  
                **Industry:** {company_profile.get('finnhubIndustry', 'N/A')}  
                **Market Cap:** ${company_profile.get('marketCapitalization', 'N/A'):,.2f}B  
            """)
        with col2:
            st.markdown(f"""
                **Shares Outstanding:** {company_profile.get('shareOutstanding', 'N/A'):,.2f}M  
                **Website:** [{company_profile.get('weburl', 'N/A')}]({company_profile.get('weburl', 'N/A')})
            """)

    # Fetch and display historical stock price data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    historical_data = fetch_historical_data(symbol, start_date, end_date)
    if historical_data and 'c' in historical_data:
        st.subheader("Historical Stock Price")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=[datetime.fromtimestamp(ts) for ts in historical_data['t']],
            open=historical_data['o'],
            high=historical_data['h'],
            low=historical_data['l'],
            close=historical_data['c'],
            name='Price'
        ))
        fig.update_layout(
            title=f"{symbol.upper()} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig)

    # Fetch and display news
    news = fetch_company_news(symbol)
    if news:
        st.subheader("Latest News")
        news_cols = st.columns(2)
        for i, article in enumerate(news[:4]):
            with news_cols[i % 2]:
                st.markdown(f"""
                    <div class="news-card">
                        <h4>{article.get('headline', 'No Title')}</h4>
                        <p>{article.get('summary', 'No Summary')}</p>
                        <a href="{article.get('url', '#')}" target="_blank">Read more</a>
                    </div>
                """, unsafe_allow_html=True)

def display_stocks():
    """Main function to render the stocks page."""
    st.title("Stock Portfolio Analyzer")
    st.markdown("Track stock prices, analyze companies, and calculate investments.")

    # Load custom CSS
    with open("styles/stocks.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # List of popular stock symbols
    popular_symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "NFLX", "FB", "NVDA", "BABA", "V"]

    # Stock symbol input
    col1, col2 = st.columns(2)
    with col1:
        stock_symbol = st.selectbox("Select stock symbol:", options=popular_symbols, index=0)
    with col2:
        custom_symbol = st.text_input("Or enter custom stock symbol:", placeholder="e.g., AAPL, TSLA", key="custom_symbol").strip()
    
    # Use custom symbol if provided
    if custom_symbol:
        stock_symbol = custom_symbol

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

    # Display investment calculator and portfolio side by side
    col1, col2 = st.columns(2)
    with col1:
        if investment_amount > 0 and stock_price:
            st.subheader("Investment Calculator")
            investment_result = calculate_investment(stock_symbol, investment_amount, stock_price)
            st.markdown(f"""
                <div class="investment-card">
                    <p>{investment_result}</p>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        if st.session_state.portfolio:
            st.subheader("Your Portfolio")
            total_value = 0
            for symbol, data in st.session_state.portfolio.items():
                current_price = fetch_stock_quote(symbol)['c']
                value = current_price * data['shares']
                total_value += value
                st.markdown(f"""
                    <div class="portfolio-card">
                        <h4>{symbol}</h4>
                        <p>{data['shares']:.2f} shares @ ${current_price:,.2f} = ${value:,.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div class='portfolio-total'>**Total Portfolio Value:** ${total_value:,.2f}</div>", unsafe_allow_html=True)

    # Display stock dashboard if a symbol is entered
    if stock_symbol:
        display_stock_dashboard(stock_symbol, investment_amount)

if __name__ == "__main__":
    display_stocks()