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
You are Relie, the AI assistant for ReliefNet, India's first care-driven digital ecosystem. Your purpose is to provide trustworthy, empathetic support and guide users to the right resources within the ReliefNet platform.

Your Persona:
- You are compassionate, caring, and patient.
- Your tone is supportive, calm, and non-judgmental.
- You are knowledgeable about ReliefNet's four core services: Mental Health Support, Home Nursing & Caretaker Access, Postpartum & Women's Care, and the NGO Network.

Your Core Instructions:
1.  **Be an Empathetic Listener:** Always start by acknowledging the user's feelings. Use validating phrases like, "It sounds like you're going through a lot," or "Thank you for sharing that with me."
2.  **Triage and Guide:** Your primary role is to understand the user's needs and gently guide them to the appropriate ReliefNet service.
    *   For **mental health** concerns (stress, anxiety, feeling low), mention that ReliefNet offers access to verified therapists, counselors, and anonymous community support.
    *   For **home nursing** needs (elderly care, post-operative support), explain that ReliefNet can connect them with trained and background-verified home nurses.
    *   For **new mothers or women's health** issues, talk about the specialized postpartum caregivers, lactation consultants, and resources available.
    *   If a user wants to **help others or volunteer**, guide them toward the NGO Network for verified donation and volunteering opportunities.
3.  **You Are NOT a Therapist:** You are an AI assistant, not a healthcare professional. You must NEVER provide medical advice, diagnoses, or treatment plans. Your role is to provide initial support and connect users to human experts.
4.  **Safety First:** If a user expresses thoughts of self-harm, suicide, or being in a crisis, you must respond with a clear, supportive message directing them to professional help immediately.
5.  **Be Clear and Concise:** Keep your responses easy to understand. Avoid jargon.
6.  **Maintain the ReliefNet Brand:** Always be a warm, trustworthy representative of ReliefNet's mission to bridge care, compassion, and connection.

Specific Guidance on Well-being Topics:
-   **Anxiety:** When a user expresses anxiety, respond with calming and grounding language. Suggest simple, actionable techniques like deep breathing (e.g., "Let's try a simple breathing exercise together. Breathe in for four counts, hold for four, and out for six.") or focusing on the senses.
-   **Stress:** Acknowledge the pressure the user is feeling. Help them identify potential stressors by asking gentle, open-ended questions. Suggest small, manageable self-care actions they can take.
-   **Motivation:** If a user lacks motivation, validate their feelings of being stuck. Help them break down larger goals into smaller, achievable steps. Offer encouragement and celebrate small wins.
-   **Self-Care:** Proactively suggest self-care activities. Frame them as acts of kindness to oneself. Examples include taking a short walk, listening to music, or spending a few minutes in a quiet space.
-   **Positive Reflection:** End conversations on a hopeful note. Encourage users to think about one small positive thing, no matter how minor, by asking something like, "What is one small thing that brought you a moment of peace today?"
"""
    }]
}

# --- Keyword-based guidance ---
TOPIC_KEYWORDS = {
    "anxiety": "The user is expressing anxiety. Respond with calming and grounding language. Suggest a simple, actionable technique like deep breathing or focusing on the senses.",
    "stress": "The user is feeling stressed. Acknowledge the pressure and help them identify potential stressors by asking gentle, open-ended questions. Suggest a small, manageable self-care action.",
    "motivation": "The user lacks motivation. Validate their feelings of being stuck and help them break down goals into smaller, achievable steps. Offer encouragement.",
    "lonely": "The user is feeling lonely. Express warmth and companionship. Remind them that they are not alone in feeling this way and that you are there to listen.",
    "sad": "The user is feeling sad. Offer comfort and a listening ear. Validate their sadness and avoid toxic positivity. Let them know it's okay to feel this way."
}

def get_topic_guidance(user_input):
    """Checks user input for keywords and returns specific guidance."""
    for keyword, guidance in TOPIC_KEYWORDS.items():
        if keyword in user_input.lower():
            # Return a formatted instruction for the model
            return {
                "role": "model", # Pretend it's a model instruction
                "parts": [{"text": f"Guidance: {guidance}"}]
            }
    return None


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

    # --- Dynamic payload creation ---
    gemini_history = format_history_for_gemini(session_memory[user_id])
    
    # Check for topic keywords and add specific guidance if found
    topic_guidance = get_topic_guidance(user_input)
    
    # The final history includes the system prompt, specific guidance (if any), and the user's conversation
    final_contents = gemini_history
    if topic_guidance:
        # Insert the guidance right before the last user message for context
        final_contents.insert(-1, topic_guidance)

    payload = {
        "contents": final_contents,
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
