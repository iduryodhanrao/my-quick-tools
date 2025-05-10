import requests
import json
import streamlit as st

url = "https://real-time-news-data.p.rapidapi.com/top-headlines"
# Function to fetch news with caching - the decorator caches the function output
# for 24 hours (86400 seconds)
@st.cache_data(ttl=86400)  # Cache data for 24 hours
def get_news(country_code):
    querystring = {"limit":"500","country":country_code,"lang":"en"}

    headers = {
        "x-rapidapi-key": "05bde85a8cmshf04501812793833p1aa983jsnede7b07be1d1",
        "x-rapidapi-host": "real-time-news-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

if __name__ == "__main__":
    # Example usage
    country_code = "IN"  # Replace with the desired country code
    news_data = get_news(country_code)
    i=0
    # Print the news data
    for article in news_data["data"]:
        print(f"- Title: {article['title']}")
        print(f"  Snippet: {article['snippet']}")
        print(f"  Published Date: {article['published_datetime_utc']}")
        print("\n" + "-"*50 + "\n")
        if i > 3: 
            break
        i += 1
