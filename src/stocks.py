import requests
import streamlit as st
import json
# Function to fetch stock data with caching - the decorator caches the function output
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_data(ticker="AAPL,MSFT,^SPX"):
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"

    querystring = {"ticker":ticker}

    headers = {
        "x-rapidapi-key": st.secrets["rapidapi_key"],
        "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Example usage
    ticker = "AAPL,GOOG"  # Replace with the desired country code
    stock_data = get_stock_data(ticker)
    i=0
    # Print the news data
    for stock in stock_data.get("body", []):
        print(f"Stock Symbol: {stock['symbol']}")
        print(f"  Company Name: {stock['longName']}")
        print(f"  Current Price: ${stock['regularMarketPrice']}")
        print(f"  Today's High: ${stock['regularMarketDayHigh']}")
        print(f"  Today's Low: ${stock['regularMarketDayLow']}")
        print(f"  52-Week Range: {stock['fiftyTwoWeekRange']}")
        