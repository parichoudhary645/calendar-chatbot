# 🚀 Railway Deployment Guide

This guide will help you deploy your Calendar AI Assistant to Railway, a modern platform that makes deployment simple and fast.

## 📋 Prerequisites

Before deploying, ensure you have:

1. ✅ **Railway Account**: Sign up at [railway.app](https://railway.app)
2. ✅ **API Keys Ready**:
   - `GROQ_API_KEY` (Primary LLM)
   - `GOOGLE_API_KEY` (Gemini fallback)
   - `OPENAI_API_KEY` (Optional fallback)
   - `ANTHROPIC_API_KEY` (Optional fallback)
3. ✅ **Google Service Account**: `service_account.json` file
4. ✅ **Git Repository**: Code committed to GitHub/GitLab
5. ✅ **Calendar Setup**: Google Calendar shared with service account email

## 🔧 Step-by-Step Deployment

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Deploy Backend

```bash
cd backend
railway init --name calendar-ai-backend
railway up
```

### Step 4: Configure Backend Environment Variables

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your `calendar-ai-backend` project
3. Go to **Variables** tab
4. Add the following environment variables:

```bash
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Step 5: Upload Service Account File

1. In the same **Variables** tab
2. Click **"New Variable"**
3. Name: `SERVICE_ACCOUNT_JSON`
4. Value: Copy the entire content of your `service_account.json` file
5. Click **"Add"**

### Step 6: Get Backend URL

1. Go to **Settings** tab
2. Copy the **Domain** URL (e.g., `https://calendar-ai-backend-production.up.railway.app`)

### Step 7: Deploy Frontend

```bash
cd ../frontend
railway init --name calendar-ai-frontend
railway up
```

### Step 8: Configure Frontend Environment Variables

1. Go to your `calendar-ai-frontend` project in Railway Dashboard
2. Go to **Variables** tab
3. Add the backend URL:

```bash
BACKEND_URL=https://your-backend-url.railway.app
```

### Step 9: Test Your Deployment

1. Go to your frontend URL
2. Test the booking functionality
3. Verify calendar integration works

## 🎯 Quick Deployment Script

Use the provided deployment script for automated deployment:

```bash
./deploy.sh
```

This script will:
- Check prerequisites
- Deploy both backend and frontend
- Provide you with the URLs
- Guide you through environment variable setup

## 🔧 Manual Deployment Commands

If you prefer manual deployment:

### Backend Deployment
```bash
cd backend
railway init --name calendar-ai-backend
railway up
```

### Frontend Deployment
```bash
cd frontend
railway init --name calendar-ai-frontend
railway up
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
| `BACKEND_URL` | ✅ | Backend service URL | `https://calendar-ai-backend-production.up.railway.app` |

## 🔍 Troubleshooting

### Common Issues

#### 1. Backend Not Starting
- Check environment variables are set correctly
- Verify `SERVICE_ACCOUNT_JSON` contains valid JSON
- Check Railway logs for error messages

#### 2. Frontend Can't Connect to Backend
- Verify `BACKEND_URL` is set correctly in frontend
- Check backend is running and accessible
- Test backend health endpoint: `https://your-backend-url/health`

#### 3. Calendar Integration Not Working
- Verify service account JSON is uploaded correctly
- Check calendar is shared with service account email
- Test with simple calendar operations

#### 4. LLM Not Responding
- Check API keys are valid and have sufficient credits
- Verify API keys are set in environment variables
- Check Railway logs for API errors

### Debugging Commands

```bash
# Check backend logs
railway logs --service calendar-ai-backend

# Check frontend logs
railway logs --service calendar-ai-frontend

# Check backend status
railway status --service calendar-ai-backend

# Check frontend status
railway status --service calendar-ai-frontend
```

## 📊 Monitoring

### Railway Dashboard Features
- **Real-time logs**: Monitor application logs
- **Metrics**: CPU, memory, and network usage
- **Deployments**: Track deployment history
- **Variables**: Manage environment variables
- **Domains**: Custom domain configuration

### Health Checks
- Backend health: `https://your-backend-url/health`
- Frontend: Access the Streamlit interface

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your Git repository:

1. Connect your GitHub/GitLab repository
2. Railway will auto-deploy on every push
3. Environment variables persist across deployments

## 💰 Cost Management

### Railway Pricing
- **Free Tier**: $5 credit monthly
- **Pay-as-you-go**: $0.000463 per GB-hour
- **Pro Plan**: $20/month for unlimited usage

### Cost Optimization
- Use free tier for development
- Monitor usage in Railway dashboard
- Set up usage alerts

## 🚀 Production Considerations

### Security
- Use strong, unique API keys
- Regularly rotate API keys
- Monitor for unusual activity
- Use Railway's built-in security features

### Performance
- Monitor response times
- Set up alerts for high latency
- Optimize LLM usage
- Use caching where appropriate

### Scalability
- Railway auto-scales based on traffic
- Monitor resource usage
- Upgrade plan if needed

## 📞 Support

### Railway Support
- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

### Application Support
- Check logs for error messages
- Verify environment variables
- Test locally before deploying
- Use the health check endpoints

## 🎉 Success Checklist

- ✅ Backend deployed and accessible
- ✅ Frontend deployed and accessible
- ✅ Environment variables configured
- ✅ Service account uploaded
- ✅ Calendar integration working
- ✅ LLM responses working
- ✅ Booking functionality tested
- ✅ Schedule queries working

Your Calendar AI Assistant is now live and ready for production use! 🚀 