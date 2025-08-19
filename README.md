AI-Powered Real-Time Market Anomaly Detector
A sophisticated, real-time data processing application designed to monitor multiple cryptocurrency markets simultaneously. This tool detects statistically significant anomalies by analyzing both price and volume data, correlates them with real-world news events via sentiment analysis, and sends instant alerts through email and SMS.

Key Features
Real-Time, Multi-Asset Monitoring: Utilizes asyncio and a single WebSocket connection to efficiently monitor multiple tickers (BTC, ETH, SOL) concurrently without being rate-limited.

Multi-Factor Anomaly Detection: Goes beyond simple price checks by implementing a robust statistical model (Z-score) that flags anomalies only when both price and trading volume show unusual behavior.

AI-Powered News Correlation: Upon detecting an anomaly, the system automatically fetches relevant news headlines from a global news API.

NLP Sentiment Analysis: Uses TextBlob to perform Natural Language Processing on news headlines, assigning a sentiment score (positive, negative, neutral) to provide context for market movements.

Persistent Data Logging: All confirmed anomalies, along with their correlated news data, are permanently stored in a local SQLite database for historical analysis.

Multi-Channel Alert System: Instantly sends detailed alert notifications via both Email (using SendGrid) and SMS (using Twilio) to keep the user informed of critical market events.

Secure Configuration: All sensitive information (API keys, personal details) is managed securely outside the main codebase using a .env file.

System Architecture
The application follows a modern, event-driven architecture:

Data Ingestion: A single, persistent WebSocket connection is established with the Finnhub API to subscribe to live trade data for multiple symbols.

Real-Time Processing: The asyncio event loop processes incoming trade data as it arrives. For each trade, the system updates a sliding window of the last 60 data points for both price and volume.

Statistical Analysis: The Z-score for both price and volume is calculated. If both scores exceed their predefined thresholds, an anomaly is flagged.

Data Enrichment: The system makes an API call to GNews to fetch a relevant news headline. It then performs sentiment analysis on this headline.

Data Persistence & Alerting: The complete anomaly record (price, volume, Z-scores, news, sentiment) is logged to the SQLite database. Simultaneously, non-blocking tasks are created to send email and SMS alerts.

Tech Stack
Programming Language: Python 3.8+

Concurrency: asyncio

Core Libraries:

websockets: For real-time data streaming.

numpy: For high-performance statistical calculations.

requests: For making HTTP requests to the news API.

textblob: For NLP sentiment analysis.

python-dotenv: For managing environment variables.

Database: sqlite3 (built-in)

Alerting APIs:

sendgrid: For reliable email delivery.

twilio: For sending SMS notifications.

Data APIs:

Finnhub: Real-time cryptocurrency trade data.

GNews: Global news headlines.

Setup and Installation Guide
Follow these steps to get the project running.

1. Prerequisites
   Python 3.8 or newer

pip (Python's package installer)

2. Clone the Repository & Create Folder Structure
   Create a project folder and the necessary files:

/stock_analyzer_project
|-- .env
|-- stock_analyzer.py
|-- read_db.py
|-- README.md

3. Register for API Keys
   You will need to sign up for the free plans on the following services:

Finnhub: finnhub.io (for market data)

GNews: gnews.io (for news headlines)

SendGrid: sendgrid.com (for sending emails)

Twilio: twilio.com (for sending SMS)

4. Configure Environment Variables
   Create a file named .env in the root of your project folder and paste the following content. Fill in all the placeholder values with your actual credentials.

# .env file

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

5. Set Up Virtual Environment & Install Dependencies
   From your terminal, inside the project folder:

# Create a virtual environment

python -m venv .venv

# Activate it (Windows)

.\.venv\Scripts\activate

# OR Activate it (macOS/Linux)

# source .venv/bin/activate

# Install all required libraries

pip install websockets numpy python-dotenv requests textblob twilio sendgrid pandas

Usage

1. Run the Main Analyzer
   To start monitoring the markets, run the main script. It will run continuously until you stop it.

python stock_analyzer.py

2. View Logged Anomalies
   After the analyzer has run and detected at least one anomaly, you can view the contents of the database with the reader script.

python read_db.py

3. Stop the Application
   To stop the main analyzer, press Ctrl+C in the terminal where it is running.

Project Report and Presentation
This project serves as the basis for the final year B.Tech evaluation. A comprehensive report has been prepared, detailing the system architecture, implementation choices, and analysis of the results collected in the SQLite database. The findings demonstrate a successful application of real-time data processing and machine learning principles to solve a complex, industry-relevant problem.
