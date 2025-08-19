# stock_analyzer.py
import asyncio
import json
import websockets
import numpy as np
from collections import deque
import datetime
import sqlite3
import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv

# For Email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# For SMS
from twilio.rest import Client

# --- 1. Configuration ---
# Load all the environment variables from the .env file
load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
STOCK_SYMBOLS = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT"]
PRICE_HISTORY_WINDOW = 60
ANOMALY_THRESHOLD_PRICE_STD = 3.0
ANOMALY_THRESHOLD_VOLUME_STD = 3.5

# Config loaded from .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

# --- 2. Database Setup ---
DB_FILE = "stock_anomalies.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY, timestamp TEXT, symbol TEXT, price REAL, volume REAL,
            z_score_price REAL, z_score_volume REAL, news_headline TEXT, sentiment_score REAL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"--> Database '{DB_FILE}' is ready.")

def log_anomaly_to_db(timestamp, symbol, price, volume, z_price, z_volume, headline, sentiment):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO anomalies (timestamp, symbol, price, volume, z_score_price, z_score_volume, news_headline, sentiment_score)
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, symbol, price, volume, z_price, z_volume, headline, sentiment))
    conn.commit()
    conn.close()

# --- 3. Alerting & News Functions ---
def send_email_alert(subject, body):
    if not all([SENDGRID_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL]):
        print("--> SendGrid credentials not configured in .env file. Skipping email alert.")
        return
    message = Mail(from_email=SENDER_EMAIL, to_emails=RECIPIENT_EMAIL, subject=subject, plain_text_content=body)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print("--> Email alert sent successfully via SendGrid.")
        else:
            print(f"--> Failed to send email via SendGrid. Status: {response.status_code}")
    except Exception as e:
        print(f"--> Failed to send email via SendGrid: {e}")

def send_sms_alert(body):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
        print("--> Twilio credentials not configured in .env file. Skipping SMS alert.")
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=RECIPIENT_PHONE_NUMBER)
        print(f"--> SMS alert sent successfully (SID: {message.sid}).")
    except Exception as e:
        print(f"--> Failed to send SMS: {e}")

def get_news_and_sentiment(symbol: str):
    query_term = symbol.split(':')[-1].replace('USDT', '').lower()
    url = f"https://gnews.io/api/v4/search?q={query_term}&lang=en&max=1&token={GNEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        if not articles: return "No recent news found.", 0.0
        headline = articles[0]['title']
        sentiment = TextBlob(headline).sentiment.polarity
        return headline, sentiment
    except requests.RequestException as e:
        print(f"--> Could not fetch news: {e}")
        return "News fetch failed.", 0.0

# --- 4. Main Application Logic ---
async def main():
    uri = f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}"
    market_data = {
        symbol: {'prices': deque(maxlen=PRICE_HISTORY_WINDOW), 'volumes': deque(maxlen=PRICE_HISTORY_WINDOW)}
        for symbol in STOCK_SYMBOLS
    }
    print("--- Starting AI-Powered Anomaly & News Correlation Detector ---")
    setup_database()
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                for symbol in STOCK_SYMBOLS:
                    await websocket.send(json.dumps({'type': 'subscribe', 'symbol': symbol}))
                    print(f"--> Subscribed to {symbol}.")
                while True:
                    message = json.loads(await websocket.recv())
                    if message.get('type') == 'trade':
                        trade_data = message['data'][-1]
                        price, volume, symbol, ts_ms = trade_data['p'], trade_data['v'], trade_data['s'], trade_data['t']
                        timestamp = datetime.datetime.fromtimestamp(ts_ms / 1000)
                        if symbol in market_data:
                            market_data[symbol]['prices'].append(price)
                            market_data[symbol]['volumes'].append(volume)
                            recent_prices = market_data[symbol]['prices']
                            if len(recent_prices) < PRICE_HISTORY_WINDOW: continue
                            prices_arr = np.array(recent_prices, dtype=float)
                            volumes_arr = np.array(market_data[symbol]['volumes'], dtype=float)
                            mean_price, std_price = np.mean(prices_arr), np.std(prices_arr)
                            mean_volume, std_volume = np.mean(volumes_arr), np.std(volumes_arr)
                            z_score_price = (price - mean_price) / std_price if std_price > 0 else 0
                            z_score_volume = (volume - mean_volume) / std_volume if std_volume > 0 else 0
                            print(f"[{timestamp.strftime('%H:%M:%S')}] [{symbol}] Price: ${price:,.2f} (Z:{z_score_price:.2f}) | Vol: {volume:.4f} (Z:{z_score_volume:.2f})")
                            if abs(z_score_price) > ANOMALY_THRESHOLD_PRICE_STD and abs(z_score_volume) > ANOMALY_THRESHOLD_VOLUME_STD:
                                ts_str_db = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                                ts_str_alert = timestamp.strftime('%H:%M:%S')
                                print("\n" + "!"*20 + f" ANOMALY DETECTED IN {symbol} " + "!"*20)
                                print(f"--> [{ts_str_alert}] Price spike with high volume detected!")
                                headline, sentiment = get_news_and_sentiment(symbol)
                                sentiment_str = "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
                                print(f"    News Headline: '{headline}' (Sentiment: {sentiment_str} [{sentiment:.2f}])")
                                log_anomaly_to_db(ts_str_db, symbol, price, volume, round(z_score_price, 2), round(z_score_volume, 2), headline, round(sentiment, 2))
                                alert_subject = f"Stock Anomaly: {symbol}"
                                alert_body = (f"Anomaly detected for {symbol} at {ts_str_alert}!\n"
                                              f"Price: ${price:,.2f} (Z: {z_score_price:.2f})\n"
                                              f"Volume: {volume:.4f} (Z: {z_score_volume:.2f})\n"
                                              f"News: {headline} (Sentiment: {sentiment:.2f})")
                                asyncio.create_task(asyncio.to_thread(send_email_alert, alert_subject, alert_body))
                                asyncio.create_task(asyncio.to_thread(send_sms_alert, alert_body))
                                print("!"*(50 + len(symbol)) + "\n")
        except Exception as e:
            print(f"An error occurred: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    if not all([FINNHUB_API_KEY, GNEWS_API_KEY]):
        print("Error: API keys are missing or invalid in your .env file. Please check.")
    else:
        asyncio.run(main())