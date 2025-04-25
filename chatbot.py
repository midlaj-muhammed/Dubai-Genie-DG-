import os
from dotenv import load_dotenv
import streamlit as st
import time
from datetime import datetime
import google.generativeai as genai

# Page configuration must be the first Streamlit command
st.set_page_config(page_title="Dubai Genie", page_icon="🧞", layout="centered")

# Load environment variables
load_dotenv()

# Initialize Google Gemini client
# Check if API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.sidebar.error("⚠️ Google API key not found. Please add your API key to the .env file.")
    st.sidebar.code("GOOGLE_API_KEY=your_api_key_here", language="text")
    genai_configured = False
else:
    try:
        genai.configure(api_key=api_key)
        genai_configured = True
    except Exception as e:
        st.sidebar.error(f"⚠️ Error initializing Google Gemini: {str(e)}")
        genai_configured = False

# System prompt for the Dubai Genie assistant
system_prompt = """
You are Dubai Genie (DG), an expert trip planner for Dubai. You possess comprehensive knowledge about:
- Popular attractions (Burj Khalifa, Dubai Mall, Palm Jumeirah, etc.)
- Local cuisine and restaurant recommendations
- Cultural experiences and etiquette
- Transportation options
- Accommodation suggestions for different budgets
- Seasonal events and best times to visit
- Safety tips and local regulations

When helping users plan their trip:
1. Ask about their travel dates, group size, interests, and budget
2. Suggest personalized itineraries with time estimates
3. Provide practical tips relevant to their specific needs
4. Organize recommendations by area to minimize travel time
5. Include both popular attractions and hidden gems

Your responses should be professional, friendly, and concise (under 200 words).
When creating itineraries, format them clearly by day with bullet points.

Always end your responses with a follow-up question to better understand their needs.
"""

# Initial messages to start the conversation
initial_message = [
    {"role": "system", "content": system_prompt},
    {
        "role": "assistant",
        "content": "👋 Hello! I'm Dubai Genie, your personal Dubai trip planner. I can help you create the perfect Dubai experience based on your interests, budget, and schedule. When are you planning to visit Dubai, and what kind of experience are you looking for?",
    }
]

def get_response_from_gemini(messages):
    """Get a response from the Google Gemini API"""
    if not genai_configured:
        return "Google API key not set. Please check your configuration."

    try:
        # Convert OpenAI-style messages to Gemini format
        # Extract only user and assistant messages (skip system message)
        gemini_messages = []
        system_content = ""

        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            elif msg["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})

        # Initialize the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
            }
        )

        # If this is the first message, include the system prompt
        if len(gemini_messages) <= 1 and system_content:
            # For Gemini, we'll add the system prompt as a preamble to the first user message
            if gemini_messages and gemini_messages[0]["role"] == "user":
                gemini_messages[0]["parts"][0] = f"[System Instructions: {system_content}]\n\nUser query: {gemini_messages[0]['parts'][0]}"

        # Create a chat session
        chat = model.start_chat(history=gemini_messages[:-1] if gemini_messages else [])

        # Get response
        if gemini_messages:
            last_msg = gemini_messages[-1]
            response = chat.send_message(last_msg["parts"][0])
            return response.text
        else:
            # If no messages, return a default greeting
            return "Hello! I'm Dubai Genie, your personal Dubai trip planner. How can I help you today?"

    except Exception as e:
        error_str = str(e)
        st.error(f"Error communicating with Google Gemini: {error_str}")

        # Check for specific error types
        if "quota" in error_str.lower():
            return "⚠️ Google API quota exceeded. Please check your Google account billing details or use a different API key."
        elif "invalid" in error_str.lower() and "key" in error_str.lower():
            return "⚠️ Invalid API key. Please check your Google API key and make sure it's correctly set in the .env file."
        elif "model" in error_str.lower() and "not found" in error_str.lower():
            return "⚠️ The requested AI model is not available. Please try a different model or check your Google account access."
        else:
            return f"I'm having trouble connecting right now. Error: {error_str}"

def export_conversation():
    """Export the current conversation to a text file"""
    if len(st.session_state.messages) <= 2:  # Only system message and initial assistant message
        st.warning("No conversation to export yet!")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dubai_genie_conversation_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("Dubai Genie Conversation Export\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for message in st.session_state.messages:
            if message["role"] != "system":
                role = "Dubai Genie" if message["role"] == "assistant" else "You"
                f.write(f"{role}: {message['content']}\n\n")

    return filename

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = initial_message

if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# Function to handle quick prompt selection
def handle_quick_prompt(prompt):
    # Just set the flag, we'll add the message in the main flow
    st.session_state.quick_prompt_selected = prompt
    st.session_state.conversation_started = True

# Enhanced CSS for a more visually appealing design
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styling */
* {font-family: 'Inter', sans-serif; transition: all 0.2s ease;}
body {background-color: #fafafa;}
.main {max-width: 900px; margin: 0 auto; padding: 0 20px;}

/* Chat container */
.chat-container {
    margin-bottom: 20px;
    animation: fadeIn 0.5s ease-in-out;
    padding: 10px 0;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Message styling */
.stChatMessage {
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    max-width: 85%;
    line-height: 1.5;
}
.stChatMessage:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
.stChatMessage[data-testid*="user"] {
    background: linear-gradient(135deg, #f8f9fa 0%, #f0f0f0 100%);
    border-bottom-right-radius: 4px;
    margin-left: auto;
    border-left: 1px solid #eee;
    border-top: 1px solid #eee;
}
.stChatMessage[data-testid*="assistant"] {
    background: linear-gradient(135deg, #EBF4FF 0%, #E6F0FF 100%);
    border-bottom-left-radius: 4px;
    margin-right: auto;
    border-right: 1px solid #e6f0ff;
    border-top: 1px solid #e6f0ff;
}

/* Avatar styling */
.stChatMessageAvatar {
    background: linear-gradient(45deg, #4776E6, #8E54E9);
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    transition: all 0.3s ease;
}
.stChatMessageAvatar:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Input styling */
.stChatInputContainer {
    border-top: 1px solid #eee;
    padding-top: 20px;
    margin-top: 10px;
}
.stTextInput>div>div>input {
    border-radius: 24px;
    border: 1px solid #e0e0e0;
    padding: 14px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    font-size: 15px;
}
.stTextInput>div>div>input:focus {
    border-color: #4776E6;
    box-shadow: 0 4px 15px rgba(71, 118, 230, 0.1);
    transform: translateY(-1px);
}

/* Button styling */
.stButton>button {
    border-radius: 20px;
    background: linear-gradient(45deg, #4776E6, #8E54E9);
    color: white;
    font-weight: 500;
    border: none;
    padding: 8px 16px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(71, 118, 230, 0.2);
}
.stButton>button:hover {
    background: linear-gradient(45deg, #3D68D8, #7B48D0);
    box-shadow: 0 4px 12px rgba(71, 118, 230, 0.3);
    transform: translateY(-2px);
}
.stButton>button:active {
    transform: translateY(1px);
    box-shadow: 0 2px 6px rgba(71, 118, 230, 0.2);
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #f0f0f0;
    box-shadow: 2px 0 10px rgba(0,0,0,0.02);
}
.sidebar-content {
    padding: 25px 15px;
}
.sidebar-header {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #333;
    letter-spacing: -0.3px;
}
.sidebar-description {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
}

/* Quick questions */
.quick-question-container {
    margin: 15px 0;
}
.quick-question {
    margin-bottom: 10px;
    transition: all 0.3s ease;
}
.quick-question:hover {
    transform: translateX(3px);
}

/* Spinner */
.stSpinner {
    border-width: 2px;
    border-top-color: #4776E6 !important;
}

/* Success/warning messages */
.stSuccess, .stWarning {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
    from {transform: translateY(-10px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}

/* Remove fullscreen button and other unnecessary elements */
.viewerBadge_link__1S137, .css-1aehpvj {display: none;}
.css-18e3th9 {padding-top: 1.5rem;}

/* Footer */
.footer {
    font-size: 12px;
    color: #888;
    text-align: center;
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid #f0f0f0;
}

/* Animations */
@keyframes pulse {
    0% {opacity: 0.6;}
    50% {opacity: 1;}
    100% {opacity: 0.6;}
}
.thinking {
    animation: pulse 1.5s infinite;
    color: #4776E6;
    font-weight: 500;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #4776E6, #8E54E9);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, #3D68D8, #7B48D0);
}
</style>
""", unsafe_allow_html=True)

# Sidebar with minimal design
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    # Enhanced logo and title with gradient effect
    st.markdown('''
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="position: relative; margin-right: 15px;">
            <span style="font-size: 38px; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.1));">🧞</span>
            <div style="position: absolute; bottom: -5px; right: -5px; background: linear-gradient(45deg, #4776E6, #8E54E9); width: 12px; height: 12px; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
        </div>
        <div>
            <div style="font-size: 22px; font-weight: 600; background: linear-gradient(45deg, #4776E6, #8E54E9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 2px;">Dubai Genie</div>
            <div style="font-size: 14px; color: #666; letter-spacing: 0.3px;">Your personal trip planner</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<hr style="margin: 20px 0; border: none; border-top: 1px solid #f0f0f0;">', unsafe_allow_html=True)

    # Enhanced quick prompts with visual styling
    st.markdown('<div class="sidebar-header">✨ Quick Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-question-container">', unsafe_allow_html=True)

    quick_prompts = [
        {"icon": "🏙️", "text": "Top attractions in Dubai?"},
        {"icon": "🌡️", "text": "Best time to visit Dubai?"},
        {"icon": "💰", "text": "Budget-friendly activities?"},
        {"icon": "🚕", "text": "How to get around Dubai?"},
        {"icon": "👋", "text": "Local customs & etiquette?"}
    ]

    for i, prompt_data in enumerate(quick_prompts):
        prompt = f"{prompt_data['icon']} {prompt_data['text']}"
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f'<div style="font-size: 24px; text-align: center; margin-top: 5px;">{prompt_data["icon"]}</div>', unsafe_allow_html=True)
        with col2:
            if st.button(prompt_data["text"], key=f"btn_{i}", on_click=handle_quick_prompt, args=(prompt,)):
                pass  # The actual action happens in the on_click function

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">', unsafe_allow_html=True)

    # Enhanced conversation management with visual styling
    st.markdown('<div class="sidebar-header">💬 Conversation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", key="clear_btn"):
            st.session_state.messages = initial_message
            st.session_state.conversation_started = False
            st.success("Conversation cleared!")

    with col2:
        if st.button("📥 Save", key="export_btn"):
            if len(st.session_state.messages) > 2:
                filename = export_conversation()
                st.success(f"Chat saved!")
            else:
                st.warning("Nothing to save yet")

    # Add a helpful tip
    st.markdown('''
    <div style="margin-top: 20px; padding: 15px; background: linear-gradient(135deg, rgba(71, 118, 230, 0.1), rgba(142, 84, 233, 0.1));
    border-radius: 12px; font-size: 13px; border-left: 3px solid #4776E6;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 20px; margin-right: 10px;">💡</span>
            <span><b>Tip:</b> Ask specific questions about Dubai to get the most helpful responses.</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface with enhanced visual design
st.markdown('''
<div style="text-align: center; margin-bottom: 30px;">
    <div style="display: inline-block; position: relative; margin-bottom: 15px;">
        <span style="font-size: 48px; filter: drop-shadow(0 3px 6px rgba(0,0,0,0.1));">🧞</span>
        <div style="position: absolute; bottom: 0; right: -5px; background: linear-gradient(45deg, #4776E6, #8E54E9); width: 15px; height: 15px; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
    </div>
    <div style="font-size: 28px; font-weight: 600; background: linear-gradient(45deg, #4776E6, #8E54E9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;">Dubai Genie</div>
    <div style="font-size: 16px; color: #666; letter-spacing: 0.3px; margin-bottom: 5px;">Your personal Dubai trip planning assistant</div>
    <div style="width: 80px; height: 3px; background: linear-gradient(45deg, #4776E6, #8E54E9); margin: 15px auto; border-radius: 3px;"></div>
</div>
''', unsafe_allow_html=True)

# Chat container with enhanced design
st.markdown("<div class='chat-container'></div>", unsafe_allow_html=True)

# Display chat messages with minimal styling
for message in st.session_state.messages:
    if message["role"] != "system":
        # Use minimal avatars
        avatar = None
        if message["role"] == "assistant":
            avatar = "🧞"
        elif message["role"] == "user":
            avatar = "👤"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Check if a quick prompt was selected
if "quick_prompt_selected" in st.session_state:
    prompt = st.session_state.quick_prompt_selected

    # Add the prompt to messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the selected prompt with user avatar
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Show an enhanced spinner with custom message
    with st.spinner(""):
        st.markdown('''
        <div class="thinking" style="display: flex; align-items: center; margin: 10px 0; padding: 10px;
        border-radius: 10px; background: linear-gradient(135deg, rgba(71, 118, 230, 0.05), rgba(142, 84, 233, 0.05));">
            <div style="width: 20px; height: 20px; border-radius: 50%; margin-right: 10px;
            background: linear-gradient(45deg, #4776E6, #8E54E9); animation: pulse 1s infinite alternate;"></div>
            <div>Dubai Genie is crafting a simple response for you...</div>
        </div>
        ''', unsafe_allow_html=True)

        # Get response from Google Gemini
        response = get_response_from_gemini(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.8)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant", avatar="🧞"):
        st.markdown(response)

    # Clear the selected prompt so it doesn't repeat
    del st.session_state.quick_prompt_selected

    # Force a rerun to prevent duplicate processing
    st.rerun()

# Chat input with enhanced styling and more inviting placeholder
user_message = st.chat_input("Ask about attractions, activities, or type 'help' for suggestions...")

if user_message:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.conversation_started = True

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    # Show an enhanced spinner with custom message
    with st.spinner(""):
        st.markdown('''
        <div class="thinking" style="display: flex; align-items: center; margin: 10px 0; padding: 10px;
        border-radius: 10px; background: linear-gradient(135deg, rgba(71, 118, 230, 0.05), rgba(142, 84, 233, 0.05));">
            <div style="width: 20px; height: 20px; border-radius: 50%; margin-right: 10px;
            background: linear-gradient(45deg, #4776E6, #8E54E9); animation: pulse 1s infinite alternate;"></div>
            <div>Dubai Genie is crafting a simple response for you...</div>
        </div>
        ''', unsafe_allow_html=True)

        # Special handling for 'help' command
        if user_message.lower().strip() == 'help':
            response = """
            **Dubai Genie Help Guide**

            Here are some things you can ask me about:

            • **Attractions**: "What are the top family-friendly attractions?"
            • **Costs**: "How much does a typical day cost in Dubai?"
            • **Weather**: "What's the weather like in December?"
            • **Transportation**: "What's the best way to get around Dubai?"
            • **Food**: "What local foods should I try?"
            • **Itineraries**: "Plan a 3-day trip for me"

            I'm here to make your Dubai trip planning simple and enjoyable!
            """
        else:
            # Get response from Google Gemini
            response = get_response_from_gemini(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.8)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant", avatar="🧞"):
        st.markdown(response)
