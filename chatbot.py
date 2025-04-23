import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
# Check if API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.sidebar.error("⚠️ OpenAI API key not found. Please add your API key to the .env file.")
    st.sidebar.code("OPENAI_API_KEY=your_api_key_here", language="text")
    client = None
else:
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"⚠️ Error initializing OpenAI client: {str(e)}")
        client = None

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

def get_response_from_openai(messages):
    """Get a response from the OpenAI API"""
    if client is None:
        return "OpenAI API key not set. Please check your configuration."

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a free/less expensive model instead of gpt-4.1
            messages=messages,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        error_str = str(e)
        st.error(f"Error communicating with OpenAI: {error_str}")

        # Check for specific error types
        if "insufficient_quota" in error_str:
            return "⚠️ OpenAI API quota exceeded. Please check your OpenAI account billing details or use a different API key."
        elif "invalid_api_key" in error_str:
            return "⚠️ Invalid API key. Please check your OpenAI API key and make sure it's correctly set in the .env file."
        elif "model_not_found" in error_str:
            return "⚠️ The requested AI model is not available. Please try a different model or check your OpenAI account access."
        else:
            return "I'm having trouble connecting right now. Please try again later."
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

# Page configuration
st.set_page_config(page_title="Dubai Genie", page_icon="🧞", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main-header {text-align: center; color: #E6B422; margin-bottom: 30px;}
.chat-container {border-radius: 10px; padding: 20px; margin-bottom: 20px;}
.stTextInput>div>div>input {border-radius: 20px;}
.user-quick-btn {margin: 5px; border-radius: 15px;}
.stButton>button {border-radius: 20px; background-color: #E6B422; color: white;}
</style>
""", unsafe_allow_html=True)



# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5605/5605056.png", width=100)
    st.title("Dubai Genie 🧞")
    st.markdown("---")

    st.subheader("About")
    st.write("Dubai Genie is your AI-powered trip planner for Dubai. Ask me anything about attractions, restaurants, activities, and more!")
    st.caption("Powered by GPT-3.5-Turbo")

    st.markdown("---")

    # Quick prompts
    st.subheader("Quick Questions")
    quick_prompts = [
        "What are the top attractions in Dubai?",
        "Best time to visit Dubai?",
        "Budget-friendly activities in Dubai?",
        "Transportation options in Dubai?",
        "Dubai cultural etiquette tips?"
    ]

    # Create columns for better button layout
    for prompt in quick_prompts:
        if st.button(prompt, key=f"btn_{prompt}", on_click=handle_quick_prompt, args=(prompt,)):
            pass  # The actual action happens in the on_click function

    st.markdown("---")

    # Conversation management
    st.subheader("Conversation")
    if st.button("Clear Conversation"):
        st.session_state.messages = initial_message
        st.session_state.conversation_started = False
        st.success("Conversation cleared!")

    if st.button("Export Conversation"):
        if len(st.session_state.messages) > 2:
            filename = export_conversation()
            st.success(f"Conversation exported to {filename}")
        else:
            st.warning("No conversation to export yet!")

# Main chat interface
st.markdown("<h1 class='main-header'>✨ Dubai Genie - Your Personal Trip Planner ✨</h1>", unsafe_allow_html=True)
st.caption("Using GPT-3.5-Turbo - Free tier model")

# Display Dubai skyline image
st.image("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80", use_container_width=True)

# Chat container
st.markdown("<div class='chat-container'></div>", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar="🧞" if message["role"] == "assistant" else None):
            st.markdown(message["content"])

# Check if a quick prompt was selected
if "quick_prompt_selected" in st.session_state:
    prompt = st.session_state.quick_prompt_selected

    # Add the prompt to messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the selected prompt
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a spinner while waiting for the response
    with st.spinner("Dubai Genie is thinking..."):
        # Get response from OpenAI
        response = get_response_from_openai(st.session_state.messages)

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

# Chat input
user_message = st.chat_input("Ask Dubai Genie anything about your trip...")

if user_message:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.conversation_started = True

    with st.chat_message("user"):
        st.markdown(user_message)

    # Show a spinner while waiting for the response
    with st.spinner("Dubai Genie is thinking..."):
        # Get response from OpenAI
        response = get_response_from_openai(st.session_state.messages)

        # Add a small delay to make the typing effect more realistic
        time.sleep(0.5)

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant", avatar="🧞"):
        st.markdown(response)
