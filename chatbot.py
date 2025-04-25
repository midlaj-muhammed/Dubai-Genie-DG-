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

# Custom CSS for minimal design
st.markdown("""
<style>
/* Main container styling */
.main {max-width: 800px; margin: 0 auto;}

/* Header styling */
.main-header {font-size: 24px; font-weight: 600; margin-bottom: 10px; color: #444;}
.sub-header {font-size: 16px; color: #666; margin-bottom: 20px;}

/* Chat container */
.chat-container {margin-bottom: 20px;}

/* Message styling */
.stChatMessage {border-radius: 8px; padding: 10px; margin-bottom: 10px;}
.stChatMessage[data-testid*="user"] {background-color: #f7f7f7;}
.stChatMessage[data-testid*="assistant"] {background-color: #f0f7ff;}

/* Input styling */
.stChatInputContainer {border-top: 1px solid #eee; padding-top: 15px;}
.stTextInput>div>div>input {border-radius: 8px; border: 1px solid #ddd; padding: 10px;}

/* Button styling */
.stButton>button {border-radius: 6px; background-color: #0084ff; color: white; font-weight: 500; border: none; transition: background-color 0.3s;}
.stButton>button:hover {background-color: #0073e6;}

/* Sidebar styling */
.css-1d391kg {background-color: #f9f9f9;}
.sidebar-content {padding: 20px 10px;}
.sidebar-header {font-size: 18px; font-weight: 600; margin-bottom: 15px; color: #444;}

/* Quick questions */
.quick-question {margin-bottom: 8px;}

/* Remove fullscreen button and other unnecessary elements */
.viewerBadge_link__1S137 {display: none;}
.css-1aehpvj {display: none;}
.css-18e3th9 {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# Sidebar with minimal design
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    # Simple logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('🧞', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="sidebar-header">Dubai Genie</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-description">Your AI trip planner for Dubai</div>', unsafe_allow_html=True)
    st.caption("Powered by Google Gemini 2.0 Flash")
    st.markdown('<hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">', unsafe_allow_html=True)

    # Quick prompts with cleaner design
    st.markdown('<div class="sidebar-header">Quick Questions</div>', unsafe_allow_html=True)

    quick_prompts = [
        "What are the top attractions in Dubai?",
        "Best time to visit Dubai?",
        "Budget-friendly activities in Dubai?",
        "Transportation options in Dubai?",
        "Dubai cultural etiquette tips?"
    ]

    for prompt in quick_prompts:
        if st.button(prompt, key=f"btn_{prompt}", on_click=handle_quick_prompt, args=(prompt,)):
            pass  # The actual action happens in the on_click function

    st.markdown('<hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">', unsafe_allow_html=True)

    # Conversation management with cleaner design
    st.markdown('<div class="sidebar-header">Conversation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear", key="clear_btn"):
            st.session_state.messages = initial_message
            st.session_state.conversation_started = False
            st.success("Cleared!")

    with col2:
        if st.button("Export", key="export_btn"):
            if len(st.session_state.messages) > 2:
                filename = export_conversation()
                st.success(f"Exported!")
            else:
                st.warning("No conversation yet")

    st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface with minimal design
st.markdown("<div class='main-header'>Dubai Genie</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Your AI-powered Dubai trip planner</div>", unsafe_allow_html=True)
st.caption("Using Google Gemini 2.0 Flash - Fast and efficient model")

# Chat container with minimal design
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

    # Show a minimal spinner while waiting for the response
    with st.spinner("Thinking..."):
        # Get response from Google Gemini
        response = get_response_from_gemini(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.5)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant", avatar="🧞"):
        st.markdown(response)

    # Clear the selected prompt so it doesn't repeat
    del st.session_state.quick_prompt_selected

    # Force a rerun to prevent duplicate processing
    st.rerun()

# Chat input with minimal styling
user_message = st.chat_input("Message Dubai Genie...")

if user_message:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.conversation_started = True

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    # Show a minimal spinner while waiting for the response
    with st.spinner("Thinking..."):
        # Get response from Google Gemini
        response = get_response_from_gemini(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.5)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant", avatar="🧞"):
        st.markdown(response)
