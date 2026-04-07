
# S-Core Pro AI Assistant 🤖
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![AI-Engine](https://img.shields.io/badge/Model-Llama%203.3%20(70B)-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20(MVC)-red.svg)
![Inference](https://img.shields.io/badge/Powered%20By-Groq%20Cloud-green.svg)
![Status](https://img.shields.io/badge/Status-Stable%20v2.5.0-brightgreen.svg)

## 📌 Overview
The **S-Core Pro AI Assistant** is a high-performance Telegram bot built for 2026 standards. It leverages the ultra-fast **Groq Cloud API** and **Llama 3.3** models to provide near-instant responses. Designed with a **Modular System Architecture**, S-Core is scalable, efficient, and ready for deployment in Termux, Linux, or Cloud environments.

---

## ⚙️ Key Features
* **🧠 Persistent Context Memory**: SQLite-backed history that allows the bot to remember past interactions using separate `user` and `assistant` roles.
* **🏗️ Modular Architecture**: Clean separation of concerns between the AI Engine, Database Management, and Telegram Handlers.
* **🌐 Real-time Web Intelligence**: Integrated search capabilities to fetch up-to-date information directly from the web using Python search engines.
* **👁️ Visual Intelligence**: Powered by `Llama-3.2-11b-vision` for advanced image analysis and technical data extraction.
* **🎨 Professional UI**: Sleek header/footer formatting (HTML-style) for a premium user experience.

---

## 📂 Project Structure
```text
S-Core-AI/
├── main.py              # System Entry Point (The Orchestrator)
├── src/
│   ├── core/            # AI Engine logic & Web Search integration
│   ├── handlers/        # Telegram Commands & Message processing
│   └── database/        # SQLite Persistence & Chat History Layer
├── screenshots/         # UI Previews & Project Gallery
└── requirements.txt     # Global dependency list

🛠 Tech Stack
 * Language: Python 3.9+
 * Inference Engine: Groq Cloud (Llama 3.3 & 3.2 Vision)
 * Bot Framework: python-telegram-bot (v20+)
 * Database: SQLite3
 * Infrastructure: Termux / Linux / Docker / Railway
## ▶️ Setup & Installation (Termux/Linux)
### 1. Clone & Navigate
git clone [https://github.com/salah619/S-Core-AI.git](https://github.com/salah619/S-Core-AI.git)
cd S-Core-AI

### 2. Environment Configuration
Create a .env file in the root directory and add your keys:
```bash
TELEGRAM_TOKEN="your_bot_token_here"
GROQ_API_KEY="your_groq_api_key_here"
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the System
```bash
python main.py
```
## 📱 واجهة البوت (Interface Preview)
<p align="center">
<img src="screenshots/score1.jpg" width="350" title="S-Core Start UI" />
<img src="screenshots/score2.jpg" width="350" title="AI Analysis Preview" />
</p>
🛡 License & Disclaimer
This project is developed for educational and professional AI implementation purposes. All data processed via Groq Cloud is subject to their privacy policy.
## 🛠️ Engineering Challenges & Solutions (The Termux Journey)
Developing **S-Core** on a mobile environment (Termux) presented unique architectural challenges that shaped the final product:

* **The Rust Dependency Barrier**: We initially faced a `Metadata-Generation-Failed` error when installing heavy search libraries (like `duckduckgo-search`) due to missing Rust compilers in Termux.
    * *Solution*: Pivot to a lightweight, pure-python search implementation (`googlesearch-python`) to ensure stability without bloated dependencies.
* **Database Schema Evolution**: Transitioning from a flat-text bot to a context-aware agent required an "on-the-fly" SQL schema migration (adding `role` columns).
    * *Solution*: Implemented a modular `DatabaseManager` that handles environment-specific resets and ensures data integrity between `user` and `assistant` contexts.
* **Resource Constraints**: To maintain high performance on mobile hardware (S24 Ultra), we optimized the **Context Window** to a sliding 6-message limit, balancing "intelligence" with "latency".

#### Developed with 💡 by: Eng. Salah Al-Wafi 🧑‍💻


