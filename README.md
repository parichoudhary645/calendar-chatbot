# Calendar AI Assistant

A production-ready conversational AI assistant for Google Calendar management, built with FastAPI, Streamlit, and modern AI technologies.

## 🚀 Features

- **Natural Language Calendar Management**: Book meetings, check schedules, and manage events through conversation
- **Real Google Calendar Integration**: Actual calendar events creation and retrieval
- **AI-Powered Understanding**: LLM integration for natural language processing
- **Modern Web Interface**: Clean, responsive chat interface
- **Production Ready**: Robust error handling and scalability

## 🛠️ Tech Stack

- **Backend**: FastAPI, Groq LLM, Google Calendar API, Langchain
- **Frontend**: Streamlit with real-time chat interface

## 📋 Prerequisites

- Python 3.10+
- Google Cloud Project with Calendar API enabled
- Google Service Account credentials
- LLM API keys (Groq, Gemini, OpenAI, or Anthropic)

## 🔧 Quick Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd "assignment chatbot"

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the backend directory:

```bash
cd backend
cp env.example .env
```

Add your API keys to `.env`:

```bash
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Set Up Google Calendar

1. Create a Google Cloud Project
2. Enable Google Calendar API
3. Create a Service Account
4. Download the service account JSON file as `service_account.json` in the backend directory
5. Share your calendar with the service account email

### 4. Start the Application

```bash
# Terminal 1: Start Backend
cd backend
python main.py

# Terminal 2: Start Frontend
cd frontend
streamlit run app.py
```

### 5. Access the Application

- **Frontend**: http://localhost:8502
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Usage Examples

### Booking Meetings
```
User: "Book a meeting tomorrow at 3pm called Team Standup"
Bot: "✅ Successfully booked 'Team Standup' for tomorrow at 3pm."
```

### Checking Schedule
```
User: "What's my schedule today?"
Bot: "📅 Here's what's on your schedule today:
• 02:00 PM: Test Meeting
• 05:00 PM: football"
```

## 🚀 Deployment

This project is optimized for **Render** deployment. See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed step-by-step instructions.

### Quick Render Deployment:
1. **Sign up at [render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Deploy backend** (root directory: `backend`)
4. **Deploy frontend** (root directory: `frontend`)
5. **Set environment variables** in Render dashboard
6. **Test your live application**

## 📚 Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Detailed project documentation and architecture
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**: Complete Render deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**: Deployment checklist and troubleshooting

## 🏗️ Project Structure

```
assignment chatbot/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── simple_llm_agent.py     # AI agent with LLM integration
│   ├── calendar_utils.py       # Google Calendar API wrapper
│   ├── service_account.json    # Google credentials
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── app.py                  # Streamlit interface
│   └── requirements.txt        # Frontend dependencies
├── README.md                   # This file
├── PROJECT_SUMMARY.md          # Detailed project documentation
├── RENDER_DEPLOYMENT.md        # Render deployment guide
└── DEPLOYMENT_CHECKLIST.md     # Deployment checklist
```

## 🔐 Security

- **Service Account Authentication**: Secure Google Calendar access
- **Environment Variables**: Secure API key management
- **CORS Configuration**: Controlled frontend-backend communication
- **Input Validation**: Sanitized user inputs

## 🔮 Future Enhancements

- Multi-calendar support
- Advanced scheduling (recurring meetings)
- Meeting optimization suggestions
- Integration with Slack, Teams, email
- Mobile application
- Voice interface
- Analytics and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for detailed documentation
2. Review the [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for deployment help
3. Open an issue in the repository

---

**Built with ❤️ using FastAPI, Streamlit, and modern AI technologies** 