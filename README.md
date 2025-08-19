🤖 AI-Powered Real-Time Market Anomaly Detector
An intelligent, real-time data analysis engine that monitors cryptocurrency markets for statistical anomalies, correlates them with global news sentiment, and sends instant multi-channel alerts.
🌟 Overview
In the volatile, 24/7 world of cryptocurrency, critical market events can happen in the blink of an eye. This project provides a powerful solution: an automated system that not only detects unusual market activity but also helps you understand the potential reasons behind it.

The application establishes a high-performance data pipeline to ingest live trade data, uses a robust statistical model to identify anomalies in both price and volume, and then enriches this data by fetching and analyzing the sentiment of related news headlines. When a significant event is confirmed, it's logged to a database and you're notified instantly via Email and SMS.

✨ Key Features
⚡ Real-Time, Multi-Asset Monitoring: Utilizes asyncio and a single WebSocket to efficiently monitor multiple tickers (BTC, ETH, SOL) concurrently.

🧠 Multi-Factor Anomaly Detection: Implements a statistical Z-score model that flags anomalies only when both price and trading volume show statistically significant deviations.

📰 AI-Powered News Correlation: Automatically fetches relevant news headlines from a global news API upon detecting an anomaly.

💬 NLP Sentiment Analysis: Uses TextBlob to perform Natural Language Processing on headlines, providing crucial context (Positive, Negative, Neutral) for market movements.

💾 Persistent Data Logging: All confirmed anomalies and their correlated news data are permanently stored in a local SQLite database for historical analysis.

🔔 Multi-Channel Alert System: Sends instant, detailed alert notifications via both Email (using SendGrid) and SMS (using Twilio).

🏗️ System Architecture
The application operates on a modern, event-driven architecture designed for high throughput and resilience.

graph TD
    A[Finnhub WebSocket] -- Live Trade Data --> B{Asyncio Event Loop};
    B -- New Trade Event --> C[State Manager - Dictionaries of Deques];
    C -- Price & Volume History --> D[Statistical Engine - NumPy];
    D -- Z-Scores --> E{Anomaly Confirmation Rule};
    E -- Anomaly Confirmed --> F[GNews API];
    F -- News Headline --> G[NLP Sentiment Analysis - TextBlob];
    G -- Enriched Data --> H[SQLite Database];
    E -- Anomaly Confirmed --> I[Alerting Subsystem];
    I -- Dispatch Email --> J[SendGrid API];
    I -- Dispatch SMS --> K[Twilio API];

🛠️ Tech Stack
This project leverages a powerful combination of modern Python libraries and external APIs.

Core Language: Python 3.8+

Concurrency: asyncio - For non-blocking, I/O-bound operations.

Networking: websockets - For high-performance, real-time data streaming.

Data Analysis: numpy - For lightning-fast statistical calculations.

NLP: textblob - For simple and effective sentiment analysis.

Database: sqlite3 - For lightweight, serverless, persistent data storage.

Alerting APIs: sendgrid (Email) & twilio (SMS) - For reliable, professional-grade notifications.

Configuration: python-dotenv - For securely managing API keys and secrets.

🚀 Getting Started
Follow these steps to get the project up and running on your local machine.

1. Prerequisites
Python 3.8 or newer

Git

2. Setup & Installation
<details>
<summary><strong>Click here for a step-by-step setup guide</strong></summary>

Clone the Repository

git clone https://github.com/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector.git
cd Real-Time-Stock-Anomaly-Detector

Create and Activate a Virtual Environment

# Create the environment
python -m venv .venv

# Activate on Windows
.\.venv\Scripts\activate

# Activate on macOS/Linux
# source .venv/bin/activate

Install Dependencies

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file for this command to work. See section below.)

Configure Your Credentials

Create a file named .env in the project root.

Copy the contents of .env.example into it.

Fill in all your API keys and personal details.

</details>

3. Creating requirements.txt
To make installation easier for others, create a requirements.txt file with the following content:

websockets
numpy
python-dotenv
requests
textblob
twilio
sendgrid
pandas

4. Configuration (.env file)
Your .env file must be filled out with your secret keys. Use the following template:

# --- API KEYS ---
FINNHUB_API_KEY="PASTE_YOUR_FINNHUB_API_KEY_HERE"
GNEWS_API_KEY="PASTE_YOUR_GNEWS_API_KEY_HERE"

# --- EMAIL SETTINGS (SENDGRID) ---
SENDGRID_API_KEY="PASTE_YOUR_SENDGRID_API_KEY_HERE"
SENDER_EMAIL="your_verified_sender_email@example.com"
RECIPIENT_EMAIL="your_personal_email@example.com"

# --- SMS SETTINGS (TWILIO) ---
TWILIO_ACCOUNT_SID="PASTE_YOUR_TWILIO_ACCOUNT_SID_HERE"
TWILIO_AUTH_TOKEN="PASTE_YOUR_TWILIO_AUTH_TOKEN_HERE"
TWILIO_PHONE_NUMBER="+1..." # Your Twilio phone number
RECIPIENT_PHONE_NUMBER="+91..." # Your verified personal number

🏃‍♂️ Usage
1. Run the Main Analyzer
To start monitoring the markets, run the main script from your activated virtual environment:

python stock_analyzer.py

The script will run continuously until you stop it.

2. View Logged Anomalies
After at least one anomaly has been detected, you can view the contents of the database:

python read_db.py

3. Stop the Application
To stop the main analyzer, press Ctrl+C in the terminal where it is running.

🔮 Future Scope
Interactive Web Dashboard: Build a real-time dashboard with Flask or Streamlit to visualize the data.

Machine Learning Integration: Replace the static Z-score model with an unsupervised ML model (e.g., Isolation Forest) for more adaptive detection.

Containerization: Package the application with Docker for easy deployment and scalability.
