# Dubai Genie - Your Personal Trip Planner

Dubai Genie (DG) is an AI-powered trip planning chatbot that helps you plan your perfect trip to Dubai. Using OpenAI's GPT-4.1 model, DG provides personalized travel recommendations, detailed information about attractions, and customized itineraries based on your preferences.

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

5. Run the application:
```bash
streamlit run chatbot.py
```

## Usage

1. Open your web browser and navigate to `http://localhost:8501`
2. Start chatting with Dubai Genie
3. Share your travel preferences, interests, and requirements
4. Get personalized recommendations and itineraries

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
