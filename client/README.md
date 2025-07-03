# 🤖 Relie – Emotional Support Bot

Relie is a full-stack AI-powered emotional support chatbot, built with React (frontend) and Flask (backend). Inspired by WhatsApp UI, it offers a comforting, responsive chat interface designed for users to express their feelings and receive AI-driven responses.

---

## 💡 Features

- 🧠 LLM-powered mental wellness assistant
- 📱 Mobile-responsive design (WhatsApp-like UI)
- 🌙 Dark mode toggle
- 😊 Emoji support with picker
- 💾 Download chat history
- 🗃 Save & load past chats (localStorage)
- 🌐 Multi-language response support (coming soon)
- 🔒 Clean `.gitignore` and secure API usage

---

## 🚀 Tech Stack

- **Frontend**: React, HTML5, CSS3
- **Backend**: Python, Flask, Flask-CORS
- **AI Provider**: Groq LLM API or OpenAI (selectable)
- **Deployment**: Netlify (frontend) + [Optional: Render/Railway] (backend)

---

## 🛠 Local Setup

```bash
# Clone the repo
git clone https://github.com/Siddhartha741/emotional-support-bot.git
cd emotional-support-bot

# Backend
cd server
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python app.py

# Frontend
cd ../client
npm install
npm start
