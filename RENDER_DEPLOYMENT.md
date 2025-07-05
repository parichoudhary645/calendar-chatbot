# 🚀 Render Deployment Guide

Render offers a generous free tier and is an excellent alternative to Railway.

## 📋 Prerequisites

1. ✅ **Render Account**: Sign up at [render.com](https://render.com)
2. ✅ **Git Repository**: Code committed to GitHub/GitLab
3. ✅ **API Keys Ready**:
   - `GROQ_API_KEY` (Primary LLM)
   - `GOOGLE_API_KEY` (Gemini fallback)
   - `OPENAI_API_KEY` (Optional)
   - `ANTHROPIC_API_KEY` (Optional)
4. ✅ **Google Service Account**: `service_account.json` file
5. ✅ **Calendar Setup**: Google Calendar shared with service account email

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure your code is committed to a Git repository (GitHub/GitLab).

### Step 2: Deploy Backend

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect your Git repository**
4. **Configure the service**:

   **Basic Settings:**
   - **Name**: `calendar-ai-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

5. **Click "Create Web Service"**

### Step 3: Configure Backend Environment Variables

1. Go to your backend service dashboard
2. Click **"Environment"** tab
3. Add the following variables:

```bash
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"your-project",...}
```

**Important**: For `SERVICE_ACCOUNT_JSON`, copy the entire content of your `service_account.json` file.

### Step 4: Get Backend URL

1. Wait for deployment to complete
2. Copy the **URL** from your service dashboard (e.g., `https://calendar-ai-backend.onrender.com`)

### Step 5: Deploy Frontend

1. **Go back to Render Dashboard**
2. **Click "New +"** → **"Web Service"**
3. **Connect the same Git repository**
4. **Configure the service**:

   **Basic Settings:**
   - **Name**: `calendar-ai-frontend`
   - **Environment**: `Python 3`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: `frontend`

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

5. **Click "Create Web Service"**

### Step 6: Configure Frontend Environment Variables

1. Go to your frontend service dashboard
2. Click **"Environment"** tab
3. Add the backend URL:

```bash
BACKEND_URL=https://your-backend-url.onrender.com
```

### Step 7: Test Your Deployment

1. Wait for both services to deploy
2. Test the frontend URL
3. Verify all functionality works

## 🔧 Alternative: Manual Deployment Commands

If you prefer using Render CLI:

```bash
# Install Render CLI
npm install -g @render/cli

# Login to Render
render login

# Deploy backend
cd backend
render deploy

# Deploy frontend
cd ../frontend
render deploy
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
| `BACKEND_URL` | ✅ | Backend service URL | `https://calendar-ai-backend.onrender.com` |

## 🔍 Troubleshooting

### Common Issues

#### 1. Build Failures
- Check that `requirements.txt` is in the correct directory
- Verify Python version compatibility
- Check build logs for specific errors

#### 2. Service Not Starting
- Verify start command is correct
- Check environment variables are set
- Review service logs

#### 3. Frontend Can't Connect to Backend
- Verify `BACKEND_URL` is set correctly
- Check backend is running and accessible
- Test backend health endpoint

### Debugging Commands

```bash
# Check service logs in Render Dashboard
# Go to your service → Logs tab

# Test backend health
curl https://your-backend-url.onrender.com/health

# Test frontend
curl https://your-frontend-url.onrender.com
```

## 📊 Render Free Tier Limits

- **Web Services**: 3 free services
- **Bandwidth**: 750 hours/month
- **Sleep**: Services sleep after 15 minutes of inactivity
- **Custom Domains**: Supported
- **SSL**: Automatic HTTPS

## 🚀 Advantages of Render

- **Generous Free Tier**: 3 web services free
- **Easy Setup**: Simple web interface
- **Automatic Deployments**: Deploys on Git push
- **Custom Domains**: Easy domain setup
- **SSL**: Automatic HTTPS certificates
- **Good Documentation**: Comprehensive guides

## 🎉 Success Checklist

- ✅ Backend deployed and accessible
- ✅ Frontend deployed and accessible
- ✅ Environment variables configured
- ✅ Service account uploaded
- ✅ Calendar integration working
- ✅ LLM responses working
- ✅ Booking functionality tested
- ✅ Schedule queries working

Your Calendar AI Assistant is now live on Render! 🚀 