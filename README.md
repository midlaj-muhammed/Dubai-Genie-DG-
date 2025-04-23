# Dubai Genie - Your Personal Trip Planner

Dubai Genie (DG) is an AI-powered trip planning chatbot that helps you plan your perfect trip to Dubai. Using OpenAI's GPT-4.1 model, DG provides personalized travel recommendations, detailed information about attractions, and customized itineraries based on your preferences.

The chatbot features a clean, minimal UI design inspired by modern AI assistants like ChatGPT and Gemini.

## Features

- Interactive chat interface using Streamlit
- Personalized travel recommendations
- Detailed information about Dubai attractions, restaurants, and activities
- Customized itineraries based on user preferences
- Local customs and safety tips
- Professional and friendly assistance
- Day-wise itinerary suggestions

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/midlaj-muhammed/Dubai-Genie-DG-.git
cd Dubai-Genie-DG-
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install streamlit openai python-dotenv
```

4. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

   > **IMPORTANT**: You need a valid OpenAI API key with sufficient quota to use this application. If you see an error message like "⚠️ OpenAI API quota exceeded", you'll need to:
   > - Check your OpenAI account billing status at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
   > - Add funds to your account if needed
   > - Or use a different API key with available quota

5. Run the application:
```bash
streamlit run chatbot.py
```

## Usage

1. Open your web browser and navigate to `http://localhost:8501`
2. Start chatting with Dubai Genie
3. Share your travel preferences, interests, and requirements
4. Use the Quick Questions in the sidebar for common queries
5. Get personalized recommendations and itineraries

### Troubleshooting API Issues

If you encounter API-related errors:

- **API Key Not Found**: Make sure your `.env` file exists and contains a valid API key
- **API Quota Exceeded**: Your OpenAI account has reached its usage limit. Check your billing status and add funds if needed
- **Model Not Available**: Ensure your OpenAI account has access to the GPT-4.1 model. You can modify the model in `chatbot.py` if needed

## Security

- API keys should never be committed to version control
- The `.env` file is included in `.gitignore` for security
- Keep your OpenAI API key confidential

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4.1 model
- Streamlit for the interactive chat interface
- Python-dotenv for environment variable management

## Screenshots

![Dubai Genie Screenshot](https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80)

*Dubai Genie features a clean, minimal interface for planning your perfect Dubai trip.*
