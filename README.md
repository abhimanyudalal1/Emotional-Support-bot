 **🧠 Emotional Support Chatbot – Relie**

Relie is a full-stack AI-powered **emotional support chatbot** designed to offer empathetic, safe, and non-judgmental conversations to users. Built using **React** (frontend) and **Flask** (backend), it integrates **Groq’s LLM API** to deliver thoughtful and helpful responses in real-time.

---

## 🌐 Live Application

- **Frontend (React)**: [https://emotional-support-bot.netlify.app](https://emotional-support-bot.netlify.app)  
- **Backend (Flask API)**: [https://relie-backend-zq69.onrender.com](https://relie-backend-zq69.onrender.com)

---

## ✨ Features

- 🤖 Friendly and supportive chatbot (Relie)
- 💬 Real-time conversation handling
- 😃 Emoji picker for expressive chatting
- 💡 Prompt-based suggestions
- 📜 Chat history stored locally (browser storage)
- 💾 Option to download chat transcripts as `.txt`
- 🌓 Dark / Light mode toggle
- 📱 Mobile responsive interface
- 🚨 Trigger word detection for mental health safety

---

## 🧱 Tech Stack

| Layer        | Technology            |
|--------------|------------------------|
| Frontend     | React, Emoji Picker    |
| Backend      | Flask, Groq API        |
| Styling      | CSS                    |
| Deployment   | Netlify (frontend), Render (backend) |

---

## 📂 Project Structure
reliefnet_ai_assistant/
├── client/ # React frontend
│ └── src/
│ └── App.js # Main chatbot component
├── server/ # Flask backend
│ └── app.py # REST API to handle chat
├── requirements.txt # Python backend dependencies
└── README.md # Project documentation



---

## ⚙️ Getting Started Locally

### ✅ Backend Setup (Flask)

1. Navigate to the backend directory:
   ```bash
   cd server
2.Install Python dependencies:
pip install -r requirements.txt

3.Set your Groq API key as an environment variable:
export GROQ_API_KEY=your_api_key_here   # For Linux/Mac
set GROQ_API_KEY=your_api_key_here      # For Windows CMD

4.Run the Flask server:
python app.py

**✅ Frontend Setup (React)**
1.Navigate to the client directory:
cd client

2.Install dependencies:
npm install

3.Start the React app:
npm start

4.The frontend will open at http://localhost:3000 and send requests to the Flask backend.

**📦 Environment Variables**
Ensure the following environment variable is set in your deployment (e.g., on Render):

Variable Name 	Description
GROQ_API_KEY	 Your Groq LLM API Key

**🛡️ Mental Health Safety Note**
Relie is designed with care. It monitors for trigger words like "suicide", "self-harm", or "kill myself" and responds with appropriate caution and recommendations to contact professionals. However, Relie is not a replacement for professional mental health services.


**
🙌 Author**
Developed by **Siddhartha Namilikonda**
SR University | Computer Science Engineering


**
📄 License**
This project is open source and available under the MIT License.


---

### ✅ Final Step:
Once you've added this `README.md` file in your root directory:

```bash
git add README.md
git commit -m "📘 Added complete professional README"
git push origin main
