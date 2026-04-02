# S-Core Pro AI Assistant

## 📌 Overview

The **S-Core Pro AI Assistant** is an advanced, multi-functional Telegram bot designed to provide intelligent assistance through a rich set of features. This bot integrates cutting-edge AI capabilities, including voice-to-text transcription (powered by OpenAI Whisper), real-time web search, visual analysis, and PDF content processing. It leverages SQLite for persistent data storage, ensuring a seamless and responsive user experience. The S-Core Pro AI Assistant aims to be a versatile tool for information retrieval, content understanding, and interactive communication.

## ⚙️ Features

*   **Intelligent Conversational AI**: Engages users in natural language conversations, providing accurate and contextually relevant responses.
*   **Voice-to-Text Transcription (Whisper Integration)**: Converts spoken language from audio messages into text, enabling hands-free interaction and accessibility.
*   **Real-time Web Search Capabilities**: Fetches up-to-date information from the internet to answer queries and provide comprehensive details on various topics.
*   **Visual Content Analysis**: Processes and interprets images, allowing the bot to describe visual content, identify objects, and extract relevant information from pictures.
*   **PDF Document Understanding**: Extracts and summarizes content from PDF files, making it easy to get key information from documents directly through the chat interface.
*   **Persistent Data Storage (SQLite)**: Utilizes SQLite to store user interactions, preferences, and other relevant data, ensuring continuity and personalized experiences.
*   **Telegram Bot API Integration**: Built on the Telegram Bot API for robust and reliable communication with users.

## 🛠 Tech Stack

*   **Programming Language**: Python 3.9+
*   **Telegram Bot Framework**: `python-telegram-bot`
*   **AI/ML Libraries**: OpenAI API (Whisper for ASR, GPT for conversational AI), Google Gemini API (for advanced multimodal capabilities like vision)
*   **Web Scraping/Search**: `requests`, `BeautifulSoup` (or similar for web content retrieval)
*   **PDF Processing**: `PyPDF2` (or similar for PDF text extraction)
*   **Database**: SQLite
*   **Dependency Management**: `pip`
*   **Environment Management**: `venv`

## ▶️ How to Run (for Termux/Linux Users)

To set up and run the S-Core Pro AI Assistant on your Termux or Linux environment, follow these detailed instructions:

### Prerequisites

*   **Python 3.9+**: Ensure Python version 3.9 or newer is installed.
*   **`pip`**: The Python package installer should be available.
*   For Termux users, install Python and pip using `pkg install python`.
*   A Telegram Bot Token (obtained from BotFather on Telegram).
*   OpenAI API Key and/or Google Gemini API Key for AI functionalities.

### Installation Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/salah619/S-Core-AI.git
    cd S-Core-AI
    ```

2.  **Create and Activate a Virtual Environment** (Recommended for dependency isolation):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Termux
    # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the project's root directory and add your API keys and Telegram bot token:
    ```
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # Optional, if using OpenAI models
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY" # Optional, if using Google Gemini models
    ```
    *Replace placeholders with your actual tokens and keys.*

### Running the Bot

To start the Telegram bot, execute the following command from the project's root directory:

```bash
python3 main.py
```

The bot will connect to Telegram, and you can start interacting with it through the Telegram application.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
