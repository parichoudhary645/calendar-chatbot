# 🚀 Deployment Guide - Calendar AI Assistant

This guide will help you deploy your Calendar AI Assistant to Railway, a modern cloud platform that makes deployment simple and reliable.

## 📋 Prerequisites

Before deploying, make sure you have:

1. ✅ **LLM API Keys** (at least one required):
   - **GROQ_API_KEY** (primary, recommended)
   - **GOOGLE_API_KEY** (Gemini, fallback)
   - **OPENAI_API_KEY** (OpenAI, fallback)
   - **ANTHROPIC_API_KEY** (Anthropic, fallback)

2. ✅ **Google Calendar Setup**:
   - Google Cloud Project with Calendar API enabled
   - Service Account created and JSON file downloaded
   - Calendar shared with service account email
   - `service_account.json` file in the backend directory

3. ✅ **Git Repository**: All code committed to a Git repository

## 🎯 Railway Deployment (Recommended)

Railway is the easiest platform for deployment with automatic scaling, easy environment variable management, and excellent developer experience.

### Option 1: Automated Deployment (Recommended)

We've created an automated deployment script that handles everything for you:

```bash
# Run the deployment script
./deploy.sh
```

The script will:
- Install Railway CLI if needed
- Deploy both backend and frontend
- Set up environment variables
- Provide you with the final URLs

### Option 2: Manual Deployment

If you prefer to deploy manually, follow these steps:

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Deploy Backend

```bash
cd backend
railway init --name calendar-ai-backend
railway up
```

#### Step 3: Configure Backend Environment Variables

Go to your Railway dashboard and set these variables for the backend project:

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `GOOGLE_API_KEY` | Your Gemini API key | ❌ No (fallback) |
| `OPENAI_API_KEY` | Your OpenAI API key | ❌ No (fallback) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ❌ No (fallback) |

#### Step 4: Upload Service Account File

1. Go to your Railway backend project dashboard
2. Navigate to the "Variables" tab
3. Upload your `service_account.json` file

#### Step 5: Deploy Frontend

```bash
cd frontend
railway init --name calendar-ai-frontend
railway variables set BACKEND_URL="https://your-backend-url.railway.app"
railway up
```

#### Step 6: Get Your URLs

After deployment, you'll get:
- **Backend URL**: `https://your-backend-url.railway.app`
- **Frontend URL**: `https://your-frontend-url.railway.app`

## 🔧 Environment Variables

### Backend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key (primary LLM) | `gsk_...` |
| `GOOGLE_API_KEY` | Gemini API key (fallback) | `AIza...` |
| `OPENAI_API_KEY` | OpenAI API key (fallback) | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key (fallback) | `sk-ant-...` |

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BACKEND_URL` | URL of your deployed backend | `https://your-backend.railway.app` |

## 🌐 Domain Configuration

### Custom Domain (Optional)

1. Go to your Railway project dashboard
2. Navigate to Settings > Domains
3. Add your custom domain
4. Configure DNS records as instructed

### SSL/HTTPS

Railway provides automatic SSL certificates for all deployments.

## 📊 Monitoring & Health Checks

### Health Check Endpoints

- **Backend Health**: `https://your-backend-url.railway.app/health`
- **Frontend Health**: `https://your-frontend-url.railway.app/`

### Railway Dashboard

Monitor your applications at: https://railway.app/dashboard

## 🚀 Alternative Platforms

### Render

Render offers free hosting with automatic deployments from Git.

#### Backend Deployment

1. **Create New Web Service** on Render
2. **Connect your Git repository**
3. **Configure**:
   - **Name**: `calendar-ai-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **Set Environment Variables** in the dashboard
5. **Upload** `service_account.json` file

#### Frontend Deployment

1. **Create New Web Service** on Render
2. **Configure**:
   - **Name**: `calendar-ai-frontend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Set Environment Variables**:
   - `BACKEND_URL`: Your backend URL

### Fly.io

Fly.io offers global deployment with Docker containers.

#### Create Dockerfiles

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

#### Deploy

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login to Fly
fly auth login

# Deploy Backend
cd backend
fly launch
fly secrets set GROQ_API_KEY=your_key_here
fly deploy

# Deploy Frontend
cd ../frontend
fly launch
fly deploy
```

## 🔐 Security Best Practices

### API Key Management

- ✅ Use environment variables for all API keys
- ✅ Never commit API keys to Git
- ✅ Use Railway's secure variable storage
- ✅ Rotate API keys regularly

### Google Calendar Security

- ✅ Use service account with minimal permissions
- ✅ Share only necessary calendars
- ✅ Monitor API usage and quotas

### Application Security

- ✅ Enable CORS for frontend-backend communication
- ✅ Validate all user inputs
- ✅ Implement rate limiting (Railway handles this)
- ✅ Use HTTPS for all communications

## 📈 Performance Optimization

### Railway Optimizations

- **Auto-scaling**: Railway automatically scales based on traffic
- **Edge caching**: Automatic CDN distribution
- **Database**: Railway provides managed databases if needed

### Application Optimizations

- **LLM caching**: Consider implementing response caching
- **Calendar caching**: Cache calendar data for better performance
- **Connection pooling**: Optimize database connections

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
- Check environment variables are set correctly
- Verify `service_account.json` is uploaded
- Check Railway logs for error messages

#### Frontend Can't Connect to Backend
- Verify `BACKEND_URL` environment variable is set
- Check backend is running and healthy
- Test backend URL directly in browser

#### LLM API Errors
- Verify API keys are correct and have sufficient quota
- Check API provider status pages
- Review Railway logs for detailed error messages

#### Google Calendar Errors
- Verify service account has correct permissions
- Check calendar is shared with service account email
- Verify Calendar API is enabled in Google Cloud Console

### Getting Help

1. **Check Railway Logs**: Go to your project dashboard and view logs
2. **Test Locally**: Run the application locally to isolate issues
3. **Review Documentation**: Check this guide and project documentation
4. **Community Support**: Railway has excellent community support

## 🎉 Success Metrics

### Deployment Checklist

- ✅ Backend deployed and healthy
- ✅ Frontend deployed and accessible
- ✅ Environment variables configured
- ✅ Service account file uploaded
- ✅ API keys working
- ✅ Calendar integration functional
- ✅ Chat interface responsive

### Testing Your Deployment

1. **Health Check**: Visit `/health` endpoint
2. **Chat Interface**: Test the main chat functionality
3. **Calendar Integration**: Try booking a meeting
4. **Schedule Queries**: Check schedule functionality
5. **Error Handling**: Test with invalid inputs

## 📞 Support

For deployment issues:

1. **Railway Documentation**: https://docs.railway.app/
2. **Railway Community**: https://community.railway.app/
3. **Project Issues**: Open an issue in the project repository

---

**Your Calendar AI Assistant is now ready for production use! 🚀** 