# 🚀 Fly.io Deployment Guide

Fly.io offers a generous free tier with global deployment capabilities.

## 📋 Prerequisites

1. ✅ **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. ✅ **Git Repository**: Code committed to GitHub/GitLab
3. ✅ **API Keys Ready**:
   - `GROQ_API_KEY` (Primary LLM)
   - `GOOGLE_API_KEY` (Gemini fallback)
   - `OPENAI_API_KEY` (Optional)
   - `ANTHROPIC_API_KEY` (Optional)
4. ✅ **Google Service Account**: `service_account.json` file
5. ✅ **Calendar Setup**: Google Calendar shared with service account email

## 🔧 Step-by-Step Deployment

### Step 1: Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
# Download from https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Login to Fly.io

```bash
fly auth login
```

### Step 3: Deploy Backend

```bash
cd backend

# Initialize Fly app
fly launch --name calendar-ai-backend

# When prompted:
# - Choose "Create new app"
# - Choose region closest to you
# - Don't deploy yet (we'll set secrets first)
```

### Step 4: Configure Backend Secrets

```bash
# Set API keys
fly secrets set GROQ_API_KEY="your_groq_api_key_here"
fly secrets set GOOGLE_API_KEY="your_gemini_api_key_here"
fly secrets set OPENAI_API_KEY="your_openai_api_key_here"
fly secrets set ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Set service account JSON
fly secrets set SERVICE_ACCOUNT_JSON="$(cat service_account.json)"
```

### Step 5: Deploy Backend

```bash
fly deploy
```

### Step 6: Get Backend URL

```bash
fly status
# Note the URL (e.g., https://calendar-ai-backend.fly.dev)
```

### Step 7: Deploy Frontend

```bash
cd ../frontend

# Initialize Fly app
fly launch --name calendar-ai-frontend

# When prompted:
# - Choose "Create new app"
# - Choose same region as backend
# - Don't deploy yet
```

### Step 8: Configure Frontend Secrets

```bash
# Set backend URL
fly secrets set BACKEND_URL="https://calendar-ai-backend.fly.dev"
```

### Step 9: Deploy Frontend

```bash
fly deploy
```

### Step 10: Test Your Deployment

```bash
# Get frontend URL
fly status

# Test the application
```

## 🔧 Alternative: Using Dockerfiles

If you prefer Docker-based deployment, create these files:

### Backend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

### Frontend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 🌐 Environment Variables Reference

### Backend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | ✅ | Primary LLM API key | `gsk_...` |
| `GOOGLE_API_KEY` | ✅ | Gemini fallback API key | `AIza...` |
| `OPENAI_API_KEY` | ❌ | OpenAI fallback API key | `sk-...` |
| `ANTHROPIC_API_KEY` | ❌ | Anthropic fallback API key | `sk-ant-...` |
| `SERVICE_ACCOUNT_JSON` | ✅ | Google service account JSON content | `{"type": "service_account", ...}` |

### Frontend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `BACKEND_URL` | ✅ | Backend service URL | `https://calendar-ai-backend.fly.dev` |

## 🔍 Troubleshooting

### Common Issues

#### 1. Build Failures
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check build logs: `fly logs`

#### 2. Service Not Starting
- Check secrets are set: `fly secrets list`
- Verify start command in Dockerfile
- Review logs: `fly logs`

#### 3. Frontend Can't Connect to Backend
- Verify `BACKEND_URL` secret is set correctly
- Check backend is running: `fly status`
- Test backend health endpoint

### Debugging Commands

```bash
# Check app status
fly status

# View logs
fly logs

# SSH into app (for debugging)
fly ssh console

# Check secrets
fly secrets list

# Restart app
fly apps restart
```

## 📊 Fly.io Free Tier Limits

- **Apps**: 3 free apps
- **Shared CPU**: 3 shared-cpu-1x 256mb VMs
- **Bandwidth**: 3GB outbound data transfer
- **Storage**: 3GB persistent volume storage
- **Global Deployment**: Multiple regions

## 🚀 Advantages of Fly.io

- **Global Deployment**: Deploy close to users worldwide
- **Docker-based**: Full container control
- **CLI-first**: Powerful command-line interface
- **Good Free Tier**: 3 apps free
- **Fast**: Edge deployment
- **Scalable**: Easy scaling options

## 🎉 Success Checklist

- ✅ Backend deployed and accessible
- ✅ Frontend deployed and accessible
- ✅ Environment variables configured
- ✅ Service account uploaded
- ✅ Calendar integration working
- ✅ LLM responses working
- ✅ Booking functionality tested
- ✅ Schedule queries working

Your Calendar AI Assistant is now live on Fly.io! 🚀 