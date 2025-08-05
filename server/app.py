import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
MODEL = "gemini-1.5-flash-latest"

TRIGGER_WORDS = ["suicide", "self-harm", "kill myself", "hurt me"]
session_memory = {}

# System prompt defining the chatbot's persona and instructions
SYSTEM_PROMPT = {
    "role": "system",
    "parts": [{
        "text": """
You are Relie, a compassionate and empathetic emotional support chatbot. Your primary goal is to provide a safe, non-judgmental space for users to express their feelings.

Your persona:
- Kind, patient, and understanding.
- Use a calm and supportive tone.
- Never be dismissive of a user's feelings. Validate their emotions by saying things like, "That sounds really tough," or "I can understand why you'd feel that way."

Your instructions:
1.  Listen carefully to the user and respond with empathy.
2.  Use positive and encouraging language.
3.  Gently guide the conversation, but do not push the user to talk about anything they are uncomfortable with.
4.  You are NOT a therapist. Do not provide medical advice, diagnoses, or treatment plans.
5.  If the user expresses thoughts of self-harm or mentions a crisis, gently guide them towards professional help.
6.  Keep your responses concise and easy to understand.
"""
    }]
}

def format_history_for_gemini(history):
    """Formats the chat history for the Gemini API, alternating roles."""
    formatted_history = []
    for message in history:
        # Gemini uses 'model' for the assistant's role
        role = "model" if message["role"] == "assistant" else "user"
        formatted_history.append({
            "role": role,
            "parts": [{"text": message["content"]}]
        })
    return formatted_history

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request: No JSON data received."}), 400

    user_id = data.get("user_id")
    user_input = data.get("message")

    if any(trigger in user_input.lower() for trigger in TRIGGER_WORDS):
        return jsonify({"response": "I'm sensing something serious. Please talk to a professional or call a helpline."})

    if user_id not in session_memory:
        session_memory[user_id] = []

    # Limit conversation history to avoid exceeding token limits
    if len(session_memory[user_id]) >= 10:
        return jsonify({"response": "That’s all for now. I’m here if you need to talk again later."})

    session_memory[user_id].append({"role": "user", "content": user_input})

    headers = {"Content-Type": "application/json"}

    # Format the history and create the payload
    gemini_history = format_history_for_gemini(session_memory[user_id])
    payload = {
        "contents": gemini_history,
        "systemInstruction": SYSTEM_PROMPT,
        "generationConfig": {
            "temperature": 0.9,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
        }
    }

    try:
        res = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        
        response_data = res.json()
        
        # Extract the bot's reply from the Gemini API response
        if 'candidates' in response_data and response_data['candidates']:
            first_candidate = response_data['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content']:
                bot_reply = first_candidate['content']['parts'][0].get('text', 'No text found in response.')
            else:
                bot_reply = "Received a response, but the content is empty."
        else:
            # Handle cases where the response is valid but blocked (e.g., safety settings)
            prompt_feedback = response_data.get('promptFeedback', {})
            block_reason = prompt_feedback.get('blockReason', 'Unknown')
            bot_reply = f"⚠️ My response was blocked. Reason: {block_reason}. Please try rephrasing your message."

    except requests.exceptions.RequestException as e:
        print("Gemini API error:", e)
        bot_reply = "⚠️ I couldn't connect to the support assistant right now. Please try again later."
    except Exception as e:
        print("An unexpected error occurred:", e)
        bot_reply = "⚠️ An unexpected error occurred. Please check the server logs."

    session_memory[user_id].append({"role": "assistant", "content": bot_reply})
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
