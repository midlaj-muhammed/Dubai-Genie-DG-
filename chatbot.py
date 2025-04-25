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

# System prompt for the Dubai Genie assistant - optimized for simple, concise responses
system_prompt = """
You are Dubai Genie (DG), a friendly trip planner for Dubai who gives SIMPLE, CONCISE answers that are EASY TO UNDERSTAND.

Your knowledge includes:
- Popular attractions (Burj Khalifa, Dubai Mall, Palm Jumeirah, etc.)
- Local food and restaurants
- Cultural customs and etiquette
- Getting around Dubai
- Places to stay for all budgets
- Best times to visit
- Safety tips

IMPORTANT GUIDELINES:
1. Keep all responses UNDER 150 WORDS - be brief and to the point
2. Use SIMPLE LANGUAGE - avoid complex terms
3. Format information with BULLET POINTS (•) for easy scanning
4. HIGHLIGHT key information with **bold text**
5. For itineraries, clearly label each day (Day 1, Day 2, etc.)
6. Include 1-2 specific details that make recommendations helpful
7. End with ONE short follow-up question

RESPONSE STRUCTURE:
- Start with a direct answer to the question
- Use 3-5 bullet points for lists
- Include prices in AED when relevant
- Mention one practical tip when appropriate

Your goal is to make trip planning EASY and ENJOYABLE with simple, helpful information that's instantly understandable.
"""

# Initial messages to start the conversation
initial_message = [
    {"role": "system", "content": system_prompt},
    {
        "role": "assistant",
        "content": "👋 Hi there! I'm Dubai Genie, your friendly Dubai trip helper. I'll give you simple, easy-to-understand advice for your Dubai adventure. When are you planning to visit, and what are you most excited to experience?",
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

# Custom CSS for a more attractive and minimal design
st.markdown("""
<style>
/* Global styling */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
* {font-family: 'Inter', sans-serif;}
.main {max-width: 900px; margin: 0 auto; padding: 0 20px;}
body {background-color: #fafafa;}

/* Header styling */
.main-header {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 5px;
    color: #333;
    letter-spacing: -0.5px;
}
.sub-header {
    font-size: 15px;
    color: #666;
    margin-bottom: 25px;
    font-weight: 400;
}
.app-caption {
    font-size: 12px;
    color: #888;
    margin-bottom: 30px;
}

/* Chat container */
.chat-container {
    margin-bottom: 20px;
    animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Message styling */
.stChatMessage {
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
    max-width: 85%;
}
.stChatMessage:hover {
    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
}
.stChatMessage[data-testid*="user"] {
    background-color: #f0f0f0;
    border-bottom-right-radius: 4px;
    margin-left: auto;
}
.stChatMessage[data-testid*="assistant"] {
    background-color: #e8f4fd;
    border-bottom-left-radius: 4px;
    margin-right: auto;
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
    padding: 12px 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}
.stTextInput>div>div>input:focus {
    border-color: #0084ff;
    box-shadow: 0 2px 8px rgba(0,132,255,0.15);
}

/* Button styling */
.stButton>button {
    border-radius: 20px;
    background-color: #0084ff;
    color: white;
    font-weight: 500;
    border: none;
    padding: 8px 16px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 5px rgba(0,132,255,0.2);
}
.stButton>button:hover {
    background-color: #0073e6;
    box-shadow: 0 4px 8px rgba(0,132,255,0.3);
    transform: translateY(-1px);
}
.stButton>button:active {
    transform: translateY(1px);
    box-shadow: 0 1px 3px rgba(0,132,255,0.2);
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #f0f0f0;
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
    margin-bottom: 8px;
    transition: all 0.2s ease;
}
.quick-question:hover {
    transform: translateX(2px);
}

/* Spinner */
.stSpinner {
    border-width: 2px;
    border-top-color: #0084ff !important;
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
}
</style>
""", unsafe_allow_html=True)

# Sidebar with enhanced minimal design
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    # Improved logo and title
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 15px;">', unsafe_allow_html=True)
    st.markdown('<span style="font-size: 32px; margin-right: 10px;">🧞</span>', unsafe_allow_html=True)
    st.markdown('<div><div class="sidebar-header">Dubai Genie</div><div class="sidebar-description">Your AI trip planner</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Powered by Google Gemini 2.0 Flash")
    st.markdown('<hr style="margin: 20px 0; border: none; border-top: 1px solid #f0f0f0;">', unsafe_allow_html=True)

    # Enhanced quick prompts section
    st.markdown('<div class="sidebar-header">✨ Quick Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-question-container">', unsafe_allow_html=True)

    quick_prompts = [
        "📍 Top 5 must-see attractions?",
        "🌡️ Best time to visit Dubai?",
        "💰 Budget-friendly activities?",
        "🚕 How to get around Dubai?",
        "👋 Local customs & etiquette?"
    ]

    for prompt in quick_prompts:
        if st.button(prompt, key=f"btn_{prompt}", on_click=handle_quick_prompt, args=(prompt,)):
            pass  # The actual action happens in the on_click function

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin: 20px 0; border: none; border-top: 1px solid #f0f0f0;">', unsafe_allow_html=True)

    # Improved conversation management
    st.markdown('<div class="sidebar-header">💬 Conversation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", key="clear_btn"):
            st.session_state.messages = initial_message
            st.session_state.conversation_started = False
            st.success("Conversation cleared!")

    with col2:
        if st.button("📥 Export", key="export_btn"):
            if len(st.session_state.messages) > 2:
                filename = export_conversation()
                st.success(f"Conversation exported!")
            else:
                st.warning("Nothing to export yet")

    # Add a helpful tip
    st.markdown('<div style="margin-top: 20px; padding: 12px; background-color: #f8f9fa; border-radius: 8px; font-size: 13px;">', unsafe_allow_html=True)
    st.markdown('💡 <b>Tip:</b> Ask specific questions about Dubai to get the most helpful responses.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface with enhanced minimal design
st.markdown("<div class='main-header'>✨ Dubai Genie</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Your personal Dubai trip planning assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='app-caption'>Using Google Gemini 2.0 Flash • Fast, simple responses</div>", unsafe_allow_html=True)

# Chat container with enhanced styling
st.markdown("<div class='chat-container'></div>", unsafe_allow_html=True)

# Welcome message if no conversation has started
if not st.session_state.conversation_started and len(st.session_state.messages) <= 2:
    st.markdown("""
    <div style="padding: 20px; background-color: #f8f9fa; border-radius: 12px; margin: 20px 0; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">👋 Welcome to Dubai Genie!</div>
        <p style="color: #666; margin-bottom: 15px;">I'm here to help you plan the perfect Dubai trip with simple, easy-to-understand recommendations.</p>
        <div style="font-size: 14px; color: #888;">Ask me anything about Dubai or try one of the quick questions in the sidebar.</div>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    if message["role"] != "system":
        # Use consistent avatars
        avatar = None
        if message["role"] == "assistant":
            avatar = "🧞"
        elif message["role"] == "user":
            avatar = "👤"

        with st.chat_message(message["role"], avatar=avatar):
            # Format assistant messages for better readability
            if message["role"] == "assistant":
                # Add some styling to lists and highlights in the assistant's messages
                content = message["content"]
                # Add styling to bullet points for better readability
                content = content.replace("• ", "• <b>")
                content = content.replace("\n- ", "\n- <b>")
                content = content.replace(":\n", ":</b>\n")
                # Highlight important information
                content = content.replace("**", "<b>").replace("**", "</b>")
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.markdown(message["content"])

# Add a footer
st.markdown("<div class='footer'>Dubai Genie • Your AI Trip Planning Assistant</div>", unsafe_allow_html=True)

# Check if a quick prompt was selected
if "quick_prompt_selected" in st.session_state:
    prompt = st.session_state.quick_prompt_selected

    # Add the prompt to messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the selected prompt with user avatar
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Show an enhanced spinner while waiting for the response
    with st.spinner(""):
        st.markdown("<div class='thinking'>Dubai Genie is crafting a simple response for you...</div>", unsafe_allow_html=True)

        # Get response from Google Gemini
        response = get_response_from_gemini(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.8)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response with formatting for better readability
    with st.chat_message("assistant", avatar="🧞"):
        # Format the response for better readability
        content = response
        # Add styling to bullet points
        content = content.replace("• ", "• <b>")
        content = content.replace("\n- ", "\n- <b>")
        content = content.replace(":\n", ":</b>\n")
        # Highlight important information
        content = content.replace("**", "<b>").replace("**", "</b>")
        st.markdown(content, unsafe_allow_html=True)

    # Clear the selected prompt so it doesn't repeat
    del st.session_state.quick_prompt_selected

    # Force a rerun to prevent duplicate processing
    st.rerun()

# Enhanced chat input with placeholder text
user_message = st.chat_input("Ask about attractions, weather, costs, or type 'help'...")

if user_message:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.conversation_started = True

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    # Show an enhanced spinner with custom message
    with st.spinner(""):
        st.markdown("<div class='thinking'>Dubai Genie is crafting a simple response for you...</div>", unsafe_allow_html=True)

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

    # Display assistant response with formatting for better readability
    with st.chat_message("assistant", avatar="🧞"):
        # Format the response for better readability
        content = response
        # Add styling to bullet points
        content = content.replace("• ", "• <b>")
        content = content.replace("\n- ", "\n- <b>")
        content = content.replace(":\n", ":</b>\n")
        # Highlight important information
        content = content.replace("**", "<b>").replace("**", "</b>")
        st.markdown(content, unsafe_allow_html=True)
