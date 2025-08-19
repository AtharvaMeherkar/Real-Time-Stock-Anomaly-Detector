<div align="center">

🤖 Project Sentinel: AI Anomaly Detector
Unleash the power of real-time data. Automatically detect critical market events, understand the "why" with AI-powered news analysis, and get instant alerts before anyone else.
<p align="center">
<img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
<img alt="Status" src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge"/>
<a href="https://github.com/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector/stargazers">
<img alt="Stars" src="https://img.shields.io/github/stars/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector?style=for-the-badge&logo=github&color=FFD700"/>
</a>
<a href="https://github.com/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector/network/members">
<img alt="Forks" src="https://img.shields.io/github/forks/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector?style=for-the-badge&logo=github&color=87CEEB"/>
</a>
</p>

</div>

See Sentinel in Action!
(This is where you would place a GIF of your project running)

<p align="center">
<img src="https://placehold.co/800x300/121212/FFFFFF?text=Project%20Demo%20GIF" alt="Project Demo GIF" width="800"/>
</p>
A GIF showing the terminal detecting an anomaly, followed by a phone screen receiving the SMS alert.

🎯 Why This Project?
In today's 24/7 crypto markets, information is everything. But raw data is just noise. Project Sentinel was built to cut through that noise. It's not just another data scraper—it's an intelligent agent that acts as your personal market analyst, watching multiple assets simultaneously. It uses a robust statistical model to identify events that truly matter (anomalies in both price and volume) and then does what a human analyst would: it immediately looks for a reason by scanning and analyzing the sentiment of real-world news.

This project is a showcase of building a resilient, high-performance, event-driven system that fuses data from multiple domains (market streams, news APIs, NLP) into a single, actionable insight.

✨ Core Features
<table align="center">
<tr>
<td align="center" width="200">
<img src="https://raw.githubusercontent.com/gist/AtharvaMeherkar/034b2f2b34746d00431b9d123d45388c/raw/08b982c733615456f932e650d32d3f3f3869a19d/feature1.svg" width="60">
<h3>Real-Time Engine</h3>
<p>Blazing fast, non-blocking monitoring of multiple assets using Python's asyncio.</p>
</td>
<td align="center" width="200">
<img src="https://raw.githubusercontent.com/gist/AtharvaMeherkar/034b2f2b34746d00431b9d123d45388c/raw/08b982c733615456f932e650d32d3f3f3869a19d/feature2.svg" width="60">
<h3>Multi-Factor AI</h3>
<p>Smart anomaly detection using both price and volume Z-scores to reduce false positives.</p>
</td>
<td align="center" width="200">
<img src="https://raw.githubusercontent.com/gist/AtharvaMeherkar/034b2f2b34746d00431b9d123d45388c/raw/08b982c733615456f932e650d32d3f3f3869a19d/feature3.svg" width="60">
<h3>News Correlation</h3>
<p>Automatically fetches and analyzes the sentiment of news headlines to explain market events.</p>
</td>
<td align="center" width="200">
<img src="https://raw.githubusercontent.com/gist/AtharvaMeherkar/034b2f2b34746d00431b9d123d45388c/raw/08b982c733615456f932e650d32d3f3f3869a19d/feature4.svg" width="60">
<h3>Instant Alerts</h3>
<p>Sends immediate notifications via both Email (SendGrid) and SMS (Twilio).</p>
</td>
</tr>
</table>

🏗️ Technology & Architecture
The system is built on a modern, event-driven pipeline.

  [Live Market Data]──────────┐
      (WebSocket)             │
                              ▼
                        [Asyncio Core]───(Multi-Factor Anomaly?)───┐
                              │                                    │
                              │                                    ▼
                              └──────────[Real-Time Log]      [News API] -> [NLP]
                                                                   │
                                                                   ▼
                                                          [SQLite Database] & [Alerts]
                                                              (Email/SMS)

The tech stack was chosen for performance and reliability:

Backend: Python, asyncio, websockets

Data Science: NumPy, TextBlob

Database: SQLite3

APIs: Finnhub, GNews, SendGrid, Twilio

Configuration: python-dotenv

🚀 Getting Started
Ready to launch your own Sentinel? Here's how.

<details>
<summary><strong>► Click here for the step-by-step setup guide</strong></summary>

1. Environment Setup
First, clone the repository and set up your virtual environment.

# Clone the project
git clone https://github.com/AtharvaMeherkar/Real-Time-Stock-Anomaly-Detector.git
cd Real-Time-Stock-Anomaly-Detector

# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux

2. Install Dependencies
Install all the required libraries from the requirements.txt file.

pip install -r requirements.txt

3. Configure Your Secrets
This is the most important step. You'll need API keys from four services: Finnhub, GNews, SendGrid, and Twilio.

Create a file named .env in the project root.

Copy the contents of .env.example into it.

Fill in all your API keys and personal details.

</details>

<details>
<summary><strong>► Click here to see the .env template</strong></summary>

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

</details>

🏃 Usage
1. Launch the Detector
Activate your virtual environment and run the main script. It will connect and start monitoring 24/7.

python stock_analyzer.py

2. View Logged Anomalies
After an anomaly has been detected, view the database contents with the reader script.

python read_db.py

3. Stop the Application
To stop the main analyzer, press Ctrl+C in the terminal where it is running.
