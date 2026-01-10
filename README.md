# 🏆 My Quick Tools Dashboard

A **Streamlit-powered web application** with multiple integrated tools for news, stocks, world time, image processing, and stock analysis.

## ✨ Features

### 📰 News
- **Real-time news** from Real-time-news-data API
- **Filter by country** (India, US, UK, Australia, Canada, Germany, France, Italy, Japan, China)
- **24-hour caching** for optimized API calls
- Displays source, snippet, date, and links

### 📈 Stock Market
- **Live stock prices** from Yahoo Finance
- **Multi-select ticker search** for efficient filtering
- **Grid layout** displaying multiple stocks (4 columns)
- Shows: Company name, current price, daily high/low, 52-week range
- Supports 500+ major stocks (S&P 500)

### 🌍 World Time
- **Live wall clock** showing current time across 12 major timezones
- Displays time in: US (4 zones), India, UK, Japan, Australia, UAE, Singapore, China, Russia
- **Auto-refreshing** every second
- Shows both time and date for each location

### 🖼️ Image Convert
- **Convert images to outline sketches**
- Adjustable bilateral blur kernel, sigma color, and sigma space
- Min contour area filtering
- Supports PNG, JPG, JPEG, BMP, TIFF formats
- Download converted images as PNG

### 📊 Stock Screener (OOPS)
- **Multi-stock technical analysis** with OOP structure
- **Technical indicators**: EMA-21, RSI-14, VWAP, ATR-14
- **Intelligent recommendations**: Bullish Setup, Neutral, Bearish/Weak Setup
- **Interactive candlestick charts** using Plotly
- **Date range selection** for historical analysis
- **Debug mode** for troubleshooting

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/iduryodhanrao/my-quick-tools.git
cd my-quick-tools
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run src/main_dashboard.py
```

The app will open at `http://localhost:8501`

## 📦 Dependencies

Key packages:
- **streamlit** - Web framework
- **yfinance** - Stock data
- **pandas** - Data manipulation
- **plotly** - Interactive charts
- **pytz** - Timezone handling
- **ta** - Technical analysis indicators

## 🎯 Usage

1. **Select a page** from the sidebar navigation (📌 Navigation)
2. **News**: Select country and view latest headlines
3. **Stock Market**: Multi-select tickers and view live prices
4. **World Time**: See current time across global timezones
5. **Image Convert**: Upload image, adjust settings, download outline
6. **Stock Screener**: Enter tickers, view technical analysis, and candlestick charts

## 📝 Project Structure
```
my-quick-tools/
├── src/
│   ├── main_dashboard.py    # Main application entry point
│   ├── screener.py          # Stock screener with OOP classes
│   ├── worldtime.py         # World time zone handler
│   ├── stocks.py            # Stock data fetcher
│   ├── news.py              # News API handler
│   └── cnvt_image_drawing.py # Image converter
├── requirements.txt
└── README.md
```