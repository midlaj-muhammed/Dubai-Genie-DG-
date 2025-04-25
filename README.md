# Dubai Genie - Your Personal Trip Planner

Dubai Genie (DG) is an AI-powered trip planning chatbot that helps you plan your perfect trip to Dubai. Using Google's Gemini 2.0 Flash model, DG provides personalized travel recommendations, detailed information about attractions, and customized itineraries based on your preferences.

The chatbot features a clean, minimal UI design inspired by modern AI assistants like ChatGPT and Gemini.

🌐 **[Live Demo](https://dubaigenie.streamlit.app/)**

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
pip install streamlit google-generativeai python-dotenv
```

4. Create a `.env` file in the project root with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

   > **IMPORTANT**: You need a valid Google API key to use this application. If you see an error message like "⚠️ Google API quota exceeded", you'll need to:
   > - Get a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   > - Make sure your Google account has access to Gemini models
   > - Check your Google API usage limits in your Google Cloud Console

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

- **API Key Not Found**: Make sure your `.env` file exists and contains a valid Google API key
- **API Quota Exceeded**: Your Google account may have reached its usage limit. Check your Google Cloud Console
- **Model Not Available**: Ensure your Google account has access to the Gemini 2.0 Flash model

## Security

- API keys should never be committed to version control
- The `.env` file is included in `.gitignore` for security
- Keep your Google API key confidential

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google for providing the Gemini 2.0 Flash model
- Streamlit for the interactive chat interface
- Python-dotenv for environment variable management

## Screenshots

![Dubai Genie Screenshot](https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80)

*Dubai Genie features a clean, minimal interface for planning your perfect Dubai trip.*
