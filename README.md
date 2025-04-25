# ✨ Dubai Genie - Your Personal Trip Planner 🧞‍♂️

![GitHub stars](https://img.shields.io/github/stars/midlaj-muhammed/Dubai-Genie-DG-?style=social)
![GitHub forks](https://img.shields.io/github/forks/midlaj-muhammed/Dubai-Genie-DG-?style=social)

Dubai Genie (DG) is an AI-powered trip planning chatbot that helps you plan your perfect trip to Dubai! ✈️ Using Google's Gemini 2.0 Flash model, DG provides personalized travel recommendations, detailed information about attractions, and customized itineraries based on your preferences.

The chatbot features a clean, minimal UI design inspired by modern AI assistants like ChatGPT and Gemini, making your trip planning experience smooth and enjoyable! 🌟

## 🚀 Try It Out!

🌐 **[Live Demo](https://dubaigenie.streamlit.app/)** - Plan your Dubai adventure now!

## ✨ Features

- 💬 Interactive chat interface with a beautiful, minimal design
- 🗺️ Personalized travel recommendations tailored to your interests
- 🏙️ Detailed information about Dubai attractions, restaurants, and activities
- 📅 Customized day-by-day itineraries based on your preferences
- 🧠 Simple, easy-to-understand responses with bullet points
- 🛡️ Local customs, safety tips, and cultural guidance
- 💰 Budget-friendly suggestions for every type of traveler
- 🚗 Transportation advice to navigate Dubai efficiently

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/midlaj-muhammed/Dubai-Genie-DG-.git
cd Dubai-Genie-DG-
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install streamlit google-generativeai python-dotenv
```

### 4️⃣ Set up your API key
Create a `.env` file in the project root with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

> ⚠️ **IMPORTANT**: You need a valid Google API key to use this application.
>
> 🔑 Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
>
> 📝 Make sure your Google account has access to Gemini models
>
> 📊 Monitor your usage in the Google Cloud Console

### 5️⃣ Launch the app
```bash
streamlit run chatbot.py
```

🎉 That's it! Your Dubai Genie should now be running at `http://localhost:8501`

## 🧞‍♂️ How to Use Dubai Genie

### Getting Started
1. 🌐 Open your web browser and navigate to `http://localhost:8501`
2. 👋 Say hello to Dubai Genie!
3. 🗣️ Ask specific questions about Dubai or use the Quick Questions in the sidebar
4. 🧳 Share your travel dates, interests, and budget
5. 📝 Get simple, easy-to-understand recommendations and itineraries

### Example Questions
- "What are the top 5 attractions in Dubai?"
- "When is the best time to visit Dubai?"
- "What can I do in Dubai for under 100 AED?"
- "How do I get from the airport to downtown?"
- "What should I pack for Dubai in summer?"

### 🔍 Troubleshooting

If you encounter any issues:

| Problem | Solution |
|---------|----------|
| 🔑 **API Key Not Found** | Check that your `.env` file exists and contains a valid Google API key |
| 📊 **API Quota Exceeded** | Your Google account may have reached its usage limit. Check your Google Cloud Console |
| 🤖 **Model Not Available** | Ensure your Google account has access to the Gemini 2.0 Flash model |
| 📦 **Missing Modules** | Run `pip install -r requirements.txt` to install all dependencies |

## 🔒 Security

- 🔐 API keys should **never** be committed to version control
- 📁 The `.env` file is included in `.gitignore` for security
- 🤫 Keep your Google API key confidential
- 🛡️ Consider setting usage limits in Google Cloud Console

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 🧪 Add more test cases
- 📝 Improve documentation
- 🔀 Submit pull requests

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🤖 Google for providing the Gemini 2.0 Flash model
- 🌊 Streamlit for the interactive chat interface
- 🔧 Python-dotenv for environment variable management
- 🌍 The open-source community for inspiration and support

## 📱 Screenshots

<div align="center">
  <img src="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80" alt="Dubai Genie Screenshot" width="600"/>
  <p><em>✨ Dubai Genie features a clean, minimal interface for planning your perfect Dubai trip ✨</em></p>
</div>

## 📊 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/midlaj-muhammed/Dubai-Genie-DG-)
![GitHub issues](https://img.shields.io/github/issues/midlaj-muhammed/Dubai-Genie-DG-)
![GitHub pull requests](https://img.shields.io/github/issues-pr/midlaj-muhammed/Dubai-Genie-DG-)

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/midlaj-muhammed">Midlaj Muhammed</a></p>
  <p>⭐ Star this repository if you found it helpful! ⭐</p>
</div>
