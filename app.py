import gradio as gr
import requests
import random

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

custom_css = """
/* --- Modern Clinical Theme with Better Bot Response Visibility --- */

/* Base layout */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif !important;
    background: #F6F8FA !important;
    color: #171923 !important;
}

/* Force chatbot background to be light */
.chatbot {
    background: #ffffff !important;
}

/* Force all chat messages to have proper styling */
.message {
    background: #ffffff !important;
    color: #000000 !important;
}

/* Override any dark theme */
.dark .chatbot,
.dark .message {
    background: #ffffff !important;
    color: #000000 !important;
}

/* Header container with boxes */
.header-container {
    background: #fafcff;
    border-bottom: 2px solid #E1E9F0;
    border-radius: 0 0 24px 24px;
    box-shadow: 0 2px 8px rgba(180,200,220,0.12);
    padding: 2.5rem 1.5rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    text-align: left;
}

/* Boxes around each header item */
.header-box {
    background-color: #f0f4ff;
    border: 2px solid #667eea;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 0.8rem;
    display: inline-block;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.subtitle-box {
    background-color: #e2e8f0;
    border-color: #a3bffa;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
}

/* Header text colors */
.header-box .header-title {
    color: #2d3748 !important;
    font-weight: 700 !important;
    font-size: 2.4rem !important;
    letter-spacing: -1px;
}

.subtitle-box .header-subtitle {
    color: #4a5568 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    opacity: 0.88 !important;
}

/* Main content area */
.main-content {
    background: #fff !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 32px rgba(34,68,120,0.06);
    padding: 2rem 2.5rem 2.5rem 2.5rem;
    border: 1px solid #E4EAF1;
    color: #171923 !important;
}

/* Welcome section text styling */
.main-content h3,
.main-content p,
.main-content strong,
.main-content ul,
.main-content ul li {
    color: #171923 !important;
    font-weight: 700 !important;
    background: none !important;
}
.main-content strong {
    color: #18191A !important;
}
.main-content ul li {
    background: #E6E7EB !important;
    color: #202124 !important;
    border-radius: 10px;
    padding: 0.33em 1.1em;
    margin-bottom: 0.23em !important;
    margin-right: 0.5em;
    display: inline-block;
    font-size: 1.02em;
    font-weight: 800 !important;
    box-shadow: 0 2px 8px rgba(50,60,80,0.08);
}
.main-content ul {
    margin-top: 0.5em;
    margin-bottom: 0.6em;
}
.main-content p {
    margin-bottom: 0.4em;
}

/* Sidebar styling */
.sidebar {
    background: linear-gradient(135deg, #EAF3FA 70%, #F6F8FA 100%);
    border-radius: 15px !important;
    padding: 1.5rem 1rem 2rem 1rem;
    box-shadow: 0 2px 14px rgba(128,168,198,0.07);
    color: #1a202c !important;
    border: 1px solid #E1E9F0;
}

/* Darker and bolder consultation tips text */
.sidebar .tips-list li {
    color: #1a202c !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    line-height: 1.4 !important;
}

/* Chatbot containers */
.chatbot-container {
    border: none !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 16px rgba(60,96,140,0.04);
    background: #F6F8FA !important;
    margin-bottom: 1.5rem;
}

/* Force chatbot container to white background */
.chatbot-container,
.chatbot-container > *,
.gradio-chatbot,
.gradio-chatbot > * {
    background: #ffffff !important;
    color: #000000 !important;
}

/* Chat messages styling - force white background and dark text */
.message-wrap,
.message,
.gradio-container .chatbot .message,
.gradio-container .message,
div[data-testid="chatbot"] {
    background: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
    border-radius: 10px !important;
    padding: 15px !important;
    margin: 10px !important;
}

/* Specific targeting for bot responses */
.bot-message,
.assistant-message,
.message-wrap.bot,
.message.bot {
    background: #f8f9fa !important;
    color: #000000 !important;
    border: 2px solid #007bff !important;
}

/* User messages */
.user-message,
.message-wrap.user,
.message.user {
    background: #e3f2fd !important;
    color: #000000 !important;
    border: 1px solid #2196f3 !important;
}

/* Input placeholder styling */
.input-container input::placeholder,
.input-container textarea::placeholder {
    color: #fff !important;
    opacity: 1 !important;
    font-weight: 500;
    text-shadow: 0 1px 4px rgba(40,60,120,0.18);
}

/* Input container background and text color */
.input-container input,
.input-container textarea {
    background: #2d3748 !important;
    color: #fff !important;
    border: none !important;
}

/* Input container styling */
.input-container {
    background: #2d3748 !important;
    border-radius: 15px;
    padding: 0.9rem 1.2rem;
    box-shadow: 0 2px 16px rgba(33,90,130,0.07);
    border: 2px solid #E1E9F0;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
}
.input-container:focus-within {
    border-color: #92B8ED;
    box-shadow: 0 2px 20px rgba(33,90,130,0.10);
}

/* Buttons */
.btn-primary {
    background: linear-gradient(90deg,#4896FF,#60CCF6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.68rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 1.08rem !important;
    box-shadow: 0 4px 18px rgba(74,150,255,0.08) !important;
    transition: all 0.18s !important;
}
.btn-primary:hover {
    background: linear-gradient(90deg,#3687EA,#48B6EC) !important;
    transform: translateY(-2px) scale(1.035) !important;
}
.btn-secondary {
    background: #fff !important;
    color: #4E7FC6 !important;
    border: 1.5px solid #B1D4F7 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: background 0.14s;
}
.btn-secondary:hover {
    background: #EAF3FA !important;
    border-color: #93C7F7 !important;
}

/* Tips list */
.tips-list {
    background: none;
    border-radius: 0;
    box-shadow: none;
    margin: 0;
    padding: 0 0 1rem 1rem;
    list-style-type: disc;
}
.tips-list li {
    padding: 0.18rem 0;
    border-bottom: none;
    color: #1a202c !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    line-height: 1.4 !important;
}

/* Examples container & items */
.examples-container {
    background: #f3fafd;
    border-radius: 14px;
    padding: 1.3rem;
    box-shadow: 0 2px 12px rgba(60,100,160,0.04);
    margin-top: 1.7rem;
}
.example-item {
    background: #fff;
    border: 1.5px solid #E1E9F0 !important;
    border-radius: 9px !important;
    padding: 0.65rem 1rem !important;
    margin: 0.18rem !important;
    font-size: 1.03rem !important;
    color: #325A81 !important;
    cursor: pointer !important;
    transition: background 0.14s, border 0.16s;
}
.example-item:hover {
    background: #EAF3FA !important;
    border-color: #95C5F8 !important;
    color: #25528A !important;
    transform: translateY(-1px) scale(1.01);
}

/* Disclaimer */
.disclaimer {
    background: #FFF6F4;
    border-left: 4px solid #F7BDA7;
    border-radius: 10px;
    padding: 0.95rem 1rem;
    margin: 0.8rem 0 0.7rem 0;
    color: #A55027;
    font-size: 0.95rem;
}

/* Footer */
.gradio-container > .gradio-html:last-child {
    background: #F6F8FA !important;
    color: #4371B8 !important;
    font-size: 1.01rem !important;
    border-top: 1.5px solid #E1E9F0;
}

/* Responsive for mobile */
@media (max-width: 800px) {
    .header-title { font-size: 1.65rem !important; }
    .header-container, .main-content, .sidebar, .examples-container {
        padding: 1.1rem !important;
    }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(18px);}
    to { opacity: 1; transform: none;}
}
.gradio-container > * { animation: fadeIn 0.6s;}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base(), title="Dr. Sarah - Professional Dermatology Consultation") as ui:
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
    with gr.Row(elem_classes="main-content"):
        with gr.Column(scale=3):
            gr.Markdown("""
            ### 👋 Welcome to Your Professional Dermatology Consultation

            I'm a board-certified dermatologist with over 10 years of experience helping patients 
            achieve healthy, beautiful skin. I'm here to provide expert guidance and answer your dermatological concerns.

            **What I can help you with:**
            - Skin condition analysis and general guidance  
            - Personalized skincare routine recommendations  
            - Product recommendations for your skin type  
            - When to seek in-person dermatological care  
            - Prevention strategies for common skin issues
            """)
            chatbot = gr.Chatbot(
                height=450,
                placeholder="💬 Start your consultation with the dermatology assistant.",
                show_label=False,
                avatar_images=(
                    "https://api.dicebear.com/7.x/avataaars/svg?seed=user",
                    "https://api.dicebear.com/7.x/avataaars/svg?seed=doctor&hair=shortHair&clothing=blazer&accessories=prescription02"
                ),
                elem_classes="chatbot-container",
                show_copy_button=True
            )
            with gr.Row(elem_classes="input-container"):
                msg = gr.Textbox(
                    label="",
                    placeholder="💬 Start your consultation with the dermatology assistant.",
                    lines=2,
                    scale=5,
                    show_label=False
                )
                submit_btn = gr.Button("Send Message 💬", scale=1, variant="primary", elem_classes="btn-primary")
        with gr.Column(scale=1, elem_classes="sidebar"):
            gr.HTML("""
                <h3>💡 Consultation Tips</h3>
                <div class="tips-list">
                    <li>📍 Specify the exact location of your concern</li>
                    <li>⏰ Mention how long you've had the issue</li>
                    <li>🔍 Describe symptoms (itching, pain, changes)</li>
                    <li>🧴 List current skincare products you use</li>
                    <li>⚕️ Mention any relevant medical history</li>
                    <li>📸 Describe appearance in detail</li>
                </div>
            """)
            clear = gr.Button("🗑️ Clear Consultation", variant="secondary", elem_classes="btn-secondary")
            gr.HTML("""
                <div class="disclaimer">
                    <strong>⚠️ Important Medical Disclaimer</strong><br>
                    This virtual consultation provides general information only and cannot replace professional medical diagnosis or treatment. For persistent, concerning, or worsening symptoms, please schedule an in-person appointment with a qualified dermatologist.
                </div>
            """)
            gr.Markdown("""
            ### 📞 Need Immediate Care?

            **Seek urgent medical attention if you experience:**
            - Sudden onset of severe symptoms
            - Signs of infection (fever, pus, red streaking)
            - Rapidly changing or growing lesions
            - Severe allergic reactions

            **Schedule an in-person appointment for:**
            - Mole changes or new growths
            - Persistent symptoms lasting >2 weeks
            - Skin cancer screening
            - Prescription treatments
            """)
    with gr.Row(elem_classes="examples-container"):
        gr.Examples(
            examples=[
                "I've noticed a small, dark spot on my arm that seems to have changed shape over the past month. Should I be concerned?",
                "I have persistent acne on my face and back despite trying various over-the-counter treatments. What professional options are available?",
                "My skin has become increasingly dry and irritated since winter started. What's the best approach for seasonal skin care?",
                "I develop red, itchy rashes after using certain skincare products. How can I identify and avoid triggers?",
                "What's the difference between normal aging spots and concerning skin changes I should have examined?"
            ],
            inputs=msg,
            label="💭 Common Consultation Questions:"
        )
    msg.submit(respond, [chatbot, msg], [chatbot, msg])
    submit_btn.click(respond, [chatbot, msg], [chatbot, msg])
    clear.click(clear_chat, None, chatbot)

    gr.HTML("""
        <div style="text-align: center; padding: 2rem; color: #718096; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
            <p><strong>Virtual Dermatology Assistant</strong> | Board Certified Dermatologist<br>
            Virtual Consultation Assistant • Professional Medical Guidance</p>
            <p style="font-size: 0.9rem; margin-top: 1rem;">
                This AI assistant provides educational information and general guidance. 
                Always consult with a qualified healthcare provider for medical diagnosis and treatment.
            </p>
        </div>
    """)

if __name__ == "__main__":
    ui.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=None,
        show_error=True,
        favicon_path=None,
        app_kwargs={"docs_url": None, "redoc_url": None}
    )
