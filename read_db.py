# read_db.py
import sqlite3
import pandas as pd

DB_FILE = "stock_anomalies.db"

def view_anomalies():
    """Connects to the database and prints all anomaly records using pandas for nice formatting."""
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC", conn)
        conn.close()
        
        print("--- Fetching All Logged Anomalies ---")
        if df.empty:
            print("No anomalies have been logged yet.")
            return
            
        print(df.to_string())

    except Exception as e:
        print(f"An error occurred while reading the database: {e}")
        print("Please ensure the main script has run and created the database file.")

if __name__ == "__main__":
    view_anomalies()