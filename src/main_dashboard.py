import streamlit as st
#from weather import get_weather
from stocks import get_stock_data
from news import get_news

country_codes = {
    "IN": "India",
    "US": "United States",
    "GB": "United Kingdom",
    "AU": "Australia",
    "CA": "Canada",
    "DE": "Germany",
    "FR": "France",
    "IT": "Italy",
    "JP": "Japan",
    "CN": "China"
}

top_500_stocks = {
    "MSFT": "Microsoft Corporation",
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corporation",
    "AMZN": "Amazon.com, Inc.",
    "GOOGL": "Alphabet Inc. (Class A)",
    "GOOG": "Alphabet Inc. (Class C)",
    "META": "Meta Platforms, Inc.",
    "BRK.B": "Berkshire Hathaway Inc.",
    "AVGO": "Broadcom Inc.",
    "TSLA": "Tesla, Inc.",
    "WMT": "Walmart Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "LLY": "Eli Lilly and Company",
    "V": "Visa Inc.",
    "MA": "Mastercard Incorporated",
    "NFLX": "Netflix, Inc.",
    "XOM": "Exxon Mobil Corporation",
    "COST": "Costco Wholesale Corporation",
    "ORCL": "Oracle Corporation",
    "JNJ": "Johnson & Johnson",
    "PG": "The Procter & Gamble Company",
    "HD": "The Home Depot, Inc.",
    "UNH": "UnitedHealth Group Incorporated",
    "ABBV": "AbbVie Inc.",
    "BAC": "Bank of America Corporation",
    "KO": "The Coca-Cola Company",
    "PLTR": "Palantir Technologies Inc.",
    "TMUS": "T-Mobile US, Inc.",
    "CRM": "Salesforce, Inc.",
    "PM": "Philip Morris International Inc.",
    "CVX": "Chevron Corporation",
    "WFC": "Wells Fargo & Company",
    "CSCO": "Cisco Systems, Inc.",
    "ABT": "Abbott Laboratories",
    "IBM": "International Business Machines Corporation",
    "GE": "General Electric Company",
    "MCD": "McDonald's Corporation",
    "LIN": "Linde plc",
    "NOW": "ServiceNow, Inc.",
    "AXP": "American Express Company",
    "T": "AT&T Inc.",
    "MS": "Morgan Stanley",
    "MRK": "Merck & Co., Inc.",
    "ACN": "Accenture plc",
    "ISRG": "Intuitive Surgical, Inc.",
    "DIS": "The Walt Disney Company",
    "VZ": "Verizon Communications Inc.",
    "INTU": "Intuit Inc.",
    "PEP": "PepsiCo, Inc.",
    "UBER": "Uber Technologies, Inc.",
    "RTX": "RTX Corporation",
    "BX": "Blackstone Inc."
}
st.set_page_config(
    page_title="My Quick Tools",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Create multiple tabs
tab1, tab2, tab3 = st.tabs(["📰 News", "🌦️ Weather", "📈 Stock Market"])

# News Tab
with tab1:
# Streamlit UI
    selected_country = st.selectbox("Select a Country Code:", list(country_codes.values()))
    # Get the corresponding country code
    selected_country_cd = next((k for k, v in country_codes.items() if v == selected_country), None)

    st.header("Latest News Headlines")
    news_data = get_news(selected_country_cd)
    
    for article in news_data.get("data", []):
        st.subheader(article["title"])
        st.write(f"**Source:** {article['source_name']}")
        st.write(f"**Snippet:** {article['snippet']}")
        st.write(f"**Published Date:** {article['published_datetime_utc']}")
        st.write(f"[Read More]({article['link']})")
        st.write("---")

# Weather Tab
with tab2:
    st.header("Current Weather Report")
    #weather_data = get_weather()
    #st.write(weather_data)  # Customize based on response structure

# Stocks Tab
with tab3:

    selected_ticker = st.multiselect("Select a Stock Ticker:", list(top_500_stocks.keys()))
    st.header("Live Stock Market Data")
    #selected_ticker = "AAPL,MSFT,^SPX"  # Example ticker for testing
    submitted = st.button("Get Stock Data")
    if submitted:
        # Call the function to get stock data
        print(",".join(selected_ticker))
        flattened_ticker = ",".join(selected_ticker)
        stocks_data = get_stock_data(flattened_ticker)
    else:
        # If no button is pressed, use default data
        stocks_data = get_stock_data("AAPL,MSFT,TSLA,GOOG,META,^SPX")
    # Display stock data
    # Create columns for better layout (adjust number of columns)
    num_columns = 4  # Display in two columns
    columns = st.columns(num_columns)

    # Iterate over stock data and assign each stock to a column
    for i, stock in enumerate(stocks_data.get("body", [])):
        col = columns[i % num_columns]  # Alternate between columns
        with col:
            st.markdown(f"##### **{stock['symbol']}**")  # Smaller font using markdown
            st.write(f"<small>**Company Name:** {stock['longName']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Current Price:** ${stock['regularMarketPrice']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Today's High:** ${stock['regularMarketDayHigh']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Today's Low:** ${stock['regularMarketDayLow']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**52-Week Range:** {stock['fiftyTwoWeekRange']}</small>", unsafe_allow_html=True)
            st.write("---")

    