# S-Core Pro AI Assistant 🤖
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![AI-Engine](https://img.shields.io/badge/Model-Llama%203.3%20(70B)-orange.svg)
![Inference](https://img.shields.io/badge/Powered%20By-Groq%20Cloud-green.svg)

## 📌 Overview
The **S-Core Pro AI Assistant** is a high-performance Telegram bot built for 2026 standards. It leverages the ultra-fast **Groq Cloud API** and **Llama 3.3** models to provide near-instant responses. Whether it's complex coding assistance, real-time web search, or visual analysis, S-Core is designed to be your executive AI agent.

## ⚙️ Key Features
*   **Lightning-Fast Conversational AI**: Powered by `Llama-3.3-70b-versatile` for high-reasoning tasks.
*   **Visual Intelligence**: Integrated with `Llama-3.2-11b-vision` for analyzing images and visual content.
*   **Real-time Web Search**: Uses **Tavily API** to fetch up-to-date information from the internet.
*   **Secure Infrastructure**: Environment-based configuration (Zero hardcoded keys).
*   **Persistent Memory**: SQLite-backed history for seamless user interactions.

## 🛠 Tech Stack
*   **Language**: Python 3.9+
*   **Inference Engine**: [Groq Cloud](https://groq.com/) (Llama Models)
*   **Bot Framework**: `python-telegram-bot` (v20+)
*   **Search Intelligence**: Tavily API
*   **Database**: SQLite

##   ▶️ Setup & Installation (Termux/Linux)

### 1. Clone & Navigate
```bash
git clone [https://github.com/salah619/S-Core-AI.git](https://github.com/salah619/S-Core-AI.git)
cd S-Core-AI
```
### 2. Environment Configuration
```bash
​Create a .env file in the root directory:
TELEGRAM_TOKEN="your_bot_token"
GROQ_API_KEY="your_groq_key"
ADMIN_ID=123456789
TAVILY_API_KEY="your_tavily_key" # Optional
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Bot
```bash
python3 main.py
```

## 📱 واجهة البوت (Interface)

<p align="center">
  <img src="screenshots/score1.jpg" width="300" />
  <img src="screenshots/score2.jpg" width="300" />
</p>

#### Developed by: Eng. Salah Al-Wafi 🧑‍💻
