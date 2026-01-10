import streamlit as st
from stocks import get_stock_data
from news import get_news
from cnvt_image_drawing import convert_image_bytes
from screener import StockScreener
from worldtime import CountryTime
from datetime import datetime, timedelta

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

import pandas as pd

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["📰 News", "🌍 World Time", "📈 Stock Market", "🖼️ Image Convert", "📊 Stock Screener"],
    label_visibility="collapsed",
    key="page_navigation"
)

# NEWS PAGE
if page == "📰 News":
    st.header("Latest News Headlines")
    selected_country = st.selectbox("Select a Country Code:", list(country_codes.values()))
    # Get the corresponding country code
    selected_country_cd = next((k for k, v in country_codes.items() if v == selected_country), None)

    news_data = get_news(selected_country_cd)
    
    for article in news_data.get("data", []):
        st.subheader(article["title"])
        st.write(f"**Source:** {article['source_name']}")
        st.write(f"**Snippet:** {article['snippet']}")
        st.write(f"**Published Date:** {article['published_datetime_utc']}")
        st.write(f"[Read More]({article['link']})")
        st.write("---")

# WORLD TIME PAGE
elif page == "🌍 World Time":
    st.header("🌍 World Wall Clock — Live Time Across Countries")
    
    # Auto-refresh every second
    
    #time.sleep(5)
    #st.rerun()
    
    # Countries & Timezones
    countries = [
        CountryTime("United States (New York)", "America/New_York"),
        CountryTime("United States (Chicago)", "America/Chicago"),
        CountryTime("United States (Denver)", "America/Denver"),
        CountryTime("United States (Los Angeles)", "America/Los_Angeles"),
        CountryTime("India", "Asia/Kolkata"),
        CountryTime("United Kingdom", "Europe/London"),
        CountryTime("Japan", "Asia/Tokyo"),
        CountryTime("Australia (Sydney)", "Australia/Sydney"),
        CountryTime("UAE (Dubai)", "Asia/Dubai"),
        CountryTime("Singapore", "Asia/Singapore"),
        CountryTime("China (Beijing)", "Asia/Shanghai"),
        CountryTime("Russia (Moscow)", "Europe/Moscow"),
    ]
    
    # Wall-Clock Grid Display (4 columns)
    cols = st.columns(4)
    
    for idx, c in enumerate(countries):
        with cols[idx % 4]:
            st.markdown(f"### {c.country_name}")
            st.markdown(
                f"""
                <div style="font-size:48px; font-weight:bold; margin-top:-10px;">
                    {c.get_current_time()}
                </div>
                <div style="font-size:18px; color:gray;">
                    {c.get_current_date()}
                </div>
                <hr>
                """,
                unsafe_allow_html=True
            )

# STOCKS PAGE
elif page == "📈 Stock Market":
    selected_ticker = st.multiselect("Select a Stock Ticker:", list(top_500_stocks.keys()))
    st.header("Live Stock Market Data")
    submitted = st.button("Get Stock Data")
    if submitted:
        # Call the function to get stock data
        flattened_ticker = ",".join(selected_ticker)
        stocks_data = get_stock_data(flattened_ticker)
    else:
        # If no button is pressed, use default data
        stocks_data = get_stock_data("AAPL,MSFT,TSLA,GOOG,META,^SPX")
    # Display stock data
    num_columns = 4
    columns = st.columns(num_columns)

    # Iterate over stock data and assign each stock to a column
    for i, stock in enumerate(stocks_data.get("body", [])):
        col = columns[i % num_columns]
        with col:
            st.markdown(f"##### **{stock['symbol']}**")
            st.write(f"<small>**Company Name:** {stock['longName']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Current Price:** ${stock['regularMarketPrice']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Today's High:** ${stock['regularMarketDayHigh']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**Today's Low:** ${stock['regularMarketDayLow']}</small>", unsafe_allow_html=True)
            st.write(f"<small>**52-Week Range:** {stock['fiftyTwoWeekRange']}</small>", unsafe_allow_html=True)
            st.write("---")

# IMAGE CONVERT PAGE
elif page == "🖼️ Image Convert":
    st.header("Image Convert — Outline / Sketch")
    st.write("Upload an image and convert it to a clean outline sketch.")

    # Sidebar settings - only shown on this page
    st.sidebar.markdown("### Image Convert Settings")
    blur_ksize = st.sidebar.slider("Blur kernel (bilateral d)", min_value=1, max_value=31, value=9, step=2)
    sigma_color = st.sidebar.slider("Sigma Color (bilateral)", min_value=1, max_value=200, value=75, step=1)
    sigma_space = st.sidebar.slider("Sigma Space (bilateral)", min_value=1, max_value=200, value=75, step=1)
    min_area = st.sidebar.slider("Min contour area to keep", min_value=1, max_value=5000, value=100, step=1)

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "bmp", "tiff"])
    if uploaded_file is not None:
        # Read uploaded file bytes
        input_bytes = uploaded_file.read()

        # Display original image
        st.subheader("Original Image")
        st.image(input_bytes, caption=uploaded_file.name)

        # Convert image with selected parameters
        try:
            output_png = convert_image_bytes(
                input_bytes,
                blur_ksize=blur_ksize,
                sigma_color=sigma_color,
                sigma_space=sigma_space,
                min_area=min_area,
            )
        except Exception as e:
            st.error(f"Image conversion failed: {e}")
        else:
            st.subheader("Converted Outline")
            st.image(output_png, caption="Outline", use_column_width=True)

            # Provide download button
            st.download_button(
                label="Download outline PNG",
                data=output_png,
                file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_outline.png",
                mime="image/png",
            )

# STOCK SCREENER PAGE
elif page == "📊 Stock Screener":
    st.header("📊 Multi-Stock Screener")
    
    # Sidebar settings - only shown on this page
    st.sidebar.markdown("### Stock Screener Settings")
    tickers_input = st.sidebar.text_input(
        "Tickers (comma-separated)",
        value="AAPL, MSFT, TSLA, AMZN",
        key="screener_tickers"
    )
    
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime.today() - timedelta(days=365),
        key="screener_start"
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=datetime.today(),
        key="screener_end"
    )
    
    debug = st.sidebar.checkbox("Debug Mode", value=False, key="screener_debug")
    
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    # Run Screener
    if tickers:
        screener = StockScreener(tickers, start_date, end_date, debug)
        results = screener.run()
        
        # Display Results
        if results:
            st.subheader("📊 Screener Results")
            st.info("Click on a ticker below to view its OHLCV chart")
            
            import pandas as pd
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Ticker selection for detailed chart view
            st.subheader("📈 Detailed Chart View")
            selected_ticker = st.selectbox(
                "Select a ticker to view detailed OHLCV chart:",
                options=[r["Ticker"] for r in results],
                key="screener_ticker_selector"
            )
            
            if selected_ticker and selected_ticker in screener.ticker_data:
                df_chart = screener.ticker_data[selected_ticker]
                
                # Create and display candlestick chart
                fig = screener.create_ohlcv_chart(df_chart, selected_ticker)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display OHLCV data table
                with st.expander("📋 View Raw OHLCV Data"):
                    display_df = df_chart[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                    display_df = display_df.round(2)
                    st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("No data available. Check tickers or date range.")
    else:
        st.warning("Please enter at least one ticker.")