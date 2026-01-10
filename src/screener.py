import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


# ---------------------------------------------------
# Data Loader Class
# ---------------------------------------------------
class DataLoader:
    """Handles downloading and basic data processing."""
    
    @staticmethod
    def download_data(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
        """Download OHLCV data from Yahoo Finance."""
        df = yf.download(ticker, start=start, end=end)
        
        # Fix MultiIndex columns (e.g., ('Close','AAPL'))
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df.dropna(inplace=True)
        return df


# ---------------------------------------------------
# Indicator Calculator Class
# ---------------------------------------------------
class IndicatorCalculator:
    """Calculates technical indicators."""
    
    @staticmethod
    def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Add EMA, RSI, VWAP, and ATR indicators to dataframe."""
        df = df.copy()
        
        # EMA
        df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()
        
        # RSI
        rsi = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
        df["RSI_14"] = pd.Series(rsi.values, index=df.index)
        
        # VWAP
        vwap = ta.volume.VolumeWeightedAveragePrice(
            high=df["High"], low=df["Low"], close=df["Close"], volume=df["Volume"], window=14
        ).volume_weighted_average_price()
        df["VWAP"] = pd.Series(vwap.values, index=df.index)
        
        # ATR
        atr = ta.volatility.AverageTrueRange(
            high=df["High"], low=df["Low"], close=df["Close"], window=14
        ).average_true_range()
        df["ATR_14"] = pd.Series(atr.values, index=df.index)
        
        df.dropna(inplace=True)
        return df


# ---------------------------------------------------
# Recommendation Engine Class
# ---------------------------------------------------
class RecommendationEngine:
    """Generates trading recommendations based on indicators."""
    
    @staticmethod
    def get_recommendation(row: pd.Series) -> str:
        """Generate recommendation based on technical indicators."""
        score = 0
        
        if row["Close"] > row["EMA_21"]:
            score += 1
        if 30 < row["RSI_14"] < 60:
            score += 1
        if row["Close"] > row["VWAP"]:
            score += 1
        if (row["ATR_14"] / row["Close"]) < 0.06:
            score += 1
        
        if score >= 3:
            return "Bullish Setup"
        elif score <= 1:
            return "Bearish/Weak Setup"
        else:
            return "Neutral"


# ---------------------------------------------------
# Stock Screener Class
# ---------------------------------------------------
class StockScreener:
    """Main screener that processes tickers and generates results."""
    
    def __init__(self, tickers: List[str], start_date: datetime, end_date: datetime, debug: bool = False):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.debug = debug
        self.data_loader = DataLoader()
        self.indicator_calc = IndicatorCalculator()
        self.recommendation_engine = RecommendationEngine()
        self.results = []
        self.ticker_data = {}  # Store raw data for charting
    
    def process_ticker(self, ticker: str) -> Dict:
        """Process a single ticker and return results."""
        try:
            # Download data
            df = self.data_loader.download_data(ticker, self.start_date, self.end_date)
            
            # Store raw data for later charting
            self.ticker_data[ticker] = df.copy()
            
            # Add indicators
            df = self.indicator_calc.add_indicators(df)
            latest = df.iloc[-1]
            
            # Generate recommendation
            rec = self.recommendation_engine.get_recommendation(latest)
            
            if self.debug:
                with st.expander(f"Debug: {ticker}"):
                    st.write("Columns:", df.columns.tolist())
                    st.write("Shapes:", {col: df[col].shape for col in df.columns})
                    st.write(df.tail())
            
            result = {
                "Ticker": ticker,
                "High": round(latest["High"], 2),
                "Low": round(latest["Low"], 2),
                "Open": round(latest["Open"], 2),
                "Close": round(latest["Close"], 2),
                "EMA_21": round(latest["EMA_21"], 2),
                "RSI_14": round(latest["RSI_14"], 2),
                "VWAP": round(latest["VWAP"], 2),
                "ATR_14": round(latest["ATR_14"], 2),
                "Recommendation": rec
            }
            
            return result
            
        except Exception as e:
            st.error(f"Error processing {ticker}: {e}")
            return None
    
    def run(self) -> List[Dict]:
        """Run screener on all tickers."""
        for ticker in self.tickers:
            result = self.process_ticker(ticker)
            if result:
                self.results.append(result)
        
        return self.results
    
    @staticmethod
    def create_ohlcv_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
        """Create an interactive OHLCV candlestick chart with volume."""
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name=ticker
        )])
        
        fig.update_layout(
            title=f"{ticker} - OHLCV Chart",
            yaxis_title="Stock Price (USD)",
            xaxis_title="Date",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=500,
            hovermode='x unified'
        )
        
        return fig


# ---------------------------------------------------
# Streamlit App
# ---------------------------------------------------
def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Simple Multi-Stock Screener", layout="wide")
    st.title("📈 Simple Multi-Stock Screener")
    
    # Sidebar Inputs
    tickers_input = st.sidebar.text_input(
        "Tickers (comma-separated)",
        value="AAPL, MSFT, TSLA, AMZN"
    )
    
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime.today() - timedelta(days=365)
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=datetime.today()
    )
    
    debug = st.sidebar.checkbox("Debug Mode", value=False)
    
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    # Run Screener
    if tickers:
        screener = StockScreener(tickers, start_date, end_date, debug)
        results = screener.run()
        
        # Display Results
        if results:
            st.subheader("📊 Screener Results")
            st.info("Click on a ticker below to view its OHLCV chart")
            
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Ticker selection for detailed chart view
            st.subheader("📈 Detailed Chart View")
            selected_ticker = st.selectbox(
                "Select a ticker to view detailed OHLCV chart:",
                options=[r["Ticker"] for r in results],
                key="ticker_selector"
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


if __name__ == "__main__":
    main()