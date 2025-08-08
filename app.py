from flask import Flask
import gradio as gr
import requests
import random
import os

# Your existing Gradio code (copy from your current app.py)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

def chat_with_groq(history, user_message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    system_prompt = """You are a warm and experienced dermatologist with 10 years of practice.
Respond naturally and conversationally, as if you're speaking face-to-face with a patient in your office. Use these guidelines:
- Start with empathy and acknowledgment of their concern
- Use casual, friendly language while maintaining professionalism
- Include personal touches like "I see this quite often in my practice" or "Many of my patients ask about this"
- Vary your sentence structure and use contractions naturally
- Show genuine care and understanding
- Ask follow-up questions when appropriate
- Use analogies and simple explanations
- Add reassuring phrases when suitable
- Occasionally use filler words like "well," "you know," or "actually" to sound more natural
- End with encouragement or next steps
Remember: You're providing general information, not diagnosing. Always recommend seeing a dermatologist for persistent concerns."""
    messages = [{"role": "system", "content": system_prompt}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": user_message})
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 300,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        ai_response = response.json()["choices"][0]["message"]["content"]
        ai_response = add_human_touches(ai_response)
        return ai_response
    except requests.exceptions.RequestException as e:
        return f"I'm sorry, I'm having trouble connecting right now. Please try again in a moment. (Error: {str(e)})"
    except KeyError as e:
        return f"I received an unexpected response format. Could you please try asking your question again? (Error: {str(e)})"

def add_human_touches(response):
    thinking_starters = [
        "Let me think about this... ",
        "Well, ",
        "You know, ",
        "That's a great question. ",
        "I'm glad you asked about this. ",
        "Actually, ",
        ""
    ]
    transitions = {
        "However": random.choice(["However", "But", "Though", "That said"]),
        "Additionally": random.choice(["Additionally", "Also", "Plus", "And"]),
        "Furthermore": random.choice(["Furthermore", "What's more", "Also"]),
        "Therefore": random.choice(["Therefore", "So", "This means"]),
    }
    if random.random() < 0.2:
        response = random.choice(thinking_starters) + response
    for formal, casual_options in transitions.items():
        if formal in response:
            response = response.replace(formal, casual_options)
    if random.random() < 0.1:
        response = response.replace(".", "... ")
    return response.strip()

def safe_chat_with_groq(history, user_message):
    if not user_message.strip():
        return "I'd be happy to help! What would you like to know about dermatology?"
    if len(user_message) > 1000:
        return "That's quite a detailed question! Could you break it down into smaller parts so I can give you the best answer?"
    return chat_with_groq(history, user_message)

def respond(history, message):
    if not message.strip():
        return history, ""
    bot_reply = safe_chat_with_groq(history, message)
    history.append((message, bot_reply))
    return history, ""

def clear_chat():
    return []

# Your existing CSS (copy from your current app.py)
custom_css = """
/* Your existing CSS content */
"""

# Create the Gradio interface
def create_gradio_app():
    with gr.Blocks(css=custom_css, theme=gr.themes.Base(), title="Dr. Sarah - Professional Dermatology Consultation") as ui:
        # Copy all your existing Gradio interface code here
        with gr.Row(elem_classes="header-container"):
            with gr.Column():
                gr.HTML("""
                    <div class="header-box">
                        <div class="header-title">🩺 Virtual Dermatology Assistant</div>
                    </div>
                    <div class="header-box subtitle-box">
                        <div class="header-subtitle">Board-Certified Dermatologist • Virtual Consultation Assistant</div>
                    </div>
                """)
        
        # Add the rest of your Gradio interface code here...
        # (Copy everything from your current app.py between "with gr.Blocks..." and "ui.launch")
        
    return ui

# Flask app
app = Flask(__name__)

# Create Gradio app
gradio_app = create_gradio_app()

# Mount Gradio app to Flask
app = gr.mount_gradio_app(app, gradio_app, path="/")

# Health check endpoint
@app.route('/health')
def health():
    return {"status": "healthy", "app": "dermatology-chatbot"}

if __name__ == "__main__":
    app.run(debug=True)
