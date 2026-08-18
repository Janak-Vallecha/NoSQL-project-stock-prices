import pymongo
import random
import time
from datetime import datetime

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["StockMarketDB"]
collection = db["IndexPrices"]

# Major World Indices
INDICES = ["S&P 500", "Dow Jones", "NASDAQ", "FTSE 100", "Nikkei 225", "NIFTY 50"]

def initialize_db():
    """Populates the database with initial arbitrary data."""
    collection.delete_many({}) # Clear old data for a fresh start
    initial_data = []
    for index in INDICES:
        initial_data.append({
            "index_name": index,
            "price": round(random.uniform(3000, 40000), 2),
            "timestamp": datetime.now()
        })
    collection.insert_many(initial_data)
    print("Database initialized with starting prices.")

def simulate_market():
    """Generates random price updates every few seconds."""
    print("Starting live price updates... (Ctrl+C to stop)")
    while True:
        for index in INDICES:
            # Fetch the latest price to simulate a realistic fluctuation (+/- 0.5%)
            last_entry = collection.find_one({"index_name": index}, sort=[("timestamp", -1)])
            current_price = last_entry["price"]
            change = current_price * random.uniform(-0.005, 0.005)
            new_price = round(current_price + change, 2)

            # Insert new price update
            collection.insert_one({
                "index_name": index,
                "price": new_price,
                "timestamp": datetime.now()
            })
        
        time.sleep(3) # Update every 3 seconds

if __name__ == "__main__":
    initialize_db()
    simulate_market()