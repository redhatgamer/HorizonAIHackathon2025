import streamlit as st
import finnhub
import os

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY", "cut1topr01qrsirk847gcut1topr01qrsirk8480"))

def display_stocks():
    st.title("Stocks")
    st.markdown("Stock market information and analysis will be here.")

    # Input form for stock symbol
    stock_symbol = st.text_input("Enter stock symbol:", placeholder="e.g., AAPL, TSLA")

    if stock_symbol:
        # Fetch stock price
        try:
            stock_price = finnhub_client.quote(stock_symbol)
            st.subheader(f"Stock Price for {stock_symbol.upper()}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${stock_price['c']}")
            col2.metric("High Price of the Day", f"${stock_price['h']}")
            col3.metric("Low Price of the Day", f"${stock_price['l']}")
            col1.metric("Open Price of the Day", f"${stock_price['o']}")
            col2.metric("Previous Close Price", f"${stock_price['pc']}")
        except Exception as e:
            st.error(f"Error fetching stock price: {e}")

        # Fetch company profile
        try:
            company_profile = finnhub_client.company_profile2(symbol=stock_symbol)
            st.subheader(f"Company Profile for {stock_symbol.upper()}")
            st.markdown(f"""
                **Name:** {company_profile['name']}  
                **Industry:** {company_profile['finnhubIndustry']}  
                **Market Capitalization:** ${company_profile['marketCapitalization']} billion  
                **Share Outstanding:** {company_profile['shareOutstanding']} million  
                **Website:** [Visit]({company_profile['weburl']})
            """)
        except Exception as e:
            st.error(f"Error fetching company profile: {e}")

        # Investment Calculator
        st.subheader("Investment Calculator")
        investment_amount = st.number_input("Enter the amount you want to invest (USD):", min_value=0.0, step=100.0)
        if investment_amount > 0:
            shares = investment_amount / stock_price['c']
            st.write(f"With an investment of ${investment_amount}, you can buy approximately {shares:.2f} shares of {stock_symbol.upper()} at the current price of ${stock_price['c']} per share.")

        # Fetch news
        try:
            news = finnhub_client.company_news(stock_symbol, _from="2022-01-01", to="2022-12-31")
            st.subheader(f"Latest News for {stock_symbol.upper()}")
            for article in news[:5]:  # Display the latest 5 news articles
                st.markdown(f"""
                    **{article['headline']}**  
                    {article['summary']}  
                    [Read more]({article['url']})  
                    ---
                """)
        except Exception as e:
            st.error(f"Error fetching news: {e}")