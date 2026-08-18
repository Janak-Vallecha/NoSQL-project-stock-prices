import streamlit as st
import pymongo
import pandas as pd
import time

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["StockMarketDB"]
collection = db["IndexPrices"]

st.set_page_config(page_title="Global Index Tracker", layout="wide")
st.title("📈 World Stock Market Indices (Live Simulator)")

# Placeholder for real-time updates
placeholder = st.empty()

def get_data():
    """Fetch all price updates from MongoDB."""
    cursor = collection.find().sort("timestamp", -1).limit(100)
    df = pd.DataFrame(list(cursor))
    if not df.empty:
        df = df.drop(columns=['_id'])
    return df

while True:
    data = get_data()

    with placeholder.container():
        if not data.empty:
            # Get latest price for each index
            latest_prices = data.groupby("index_name").first().reset_index()
            
            # Display Metrics
            cols = st.columns(len(latest_prices))
            for i, row in latest_prices.iterrows():
                cols[i].metric(row['index_name'], f"${row['price']}")

            # Display Chart
            st.subheader("Price Trends")
            chart_data = data.pivot(index='timestamp', columns='index_name', values='price')
            st.line_chart(chart_data)

            # Display Raw Data
            st.subheader("Recent Updates")
            st.dataframe(data.head(10), use_container_width=True)
        else:
            st.warning("No data found. Please ensure app.py is running.")

    time.sleep(2) # Refresh dashboard every 2 seconds