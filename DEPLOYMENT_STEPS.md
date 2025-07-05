# 🚀 Railway Deployment - Step by Step Guide

This guide will walk you through deploying your Calendar AI Assistant to Railway.

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] **GROQ_API_KEY** (required) - Get from https://console.groq.com/
- [ ] **GOOGLE_API_KEY** (optional) - Get from https://makersuite.google.com/app/apikey
- [ ] **service_account.json** file in the backend directory
- [ ] Your Google Calendar shared with the service account email
- [ ] All code committed to Git

## 🎯 Step-by-Step Deployment

### Step 1: Login to Railway

```bash
railway login
```

This will open your browser to authenticate with Railway.

### Step 2: Deploy Backend

```bash
cd backend
railway init --name calendar-ai-backend
railway up
```

This will:
- Create a new Railway project for your backend
- Deploy your backend code
- Give you a URL like `https://calendar-ai-backend-production.up.railway.app`

### Step 3: Configure Backend Environment Variables

1. Go to https://railway.app/dashboard
2. Click on your `calendar-ai-backend` project
3. Go to the "Variables" tab
4. Add these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `GOOGLE_API_KEY` | Your Gemini API key | ❌ No |
| `OPENAI_API_KEY` | Your OpenAI API key | ❌ No |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ❌ No |

### Step 4: Upload Service Account File

1. In the same "Variables" tab
2. Click "Add File"
3. Upload your `service_account.json` file
4. Name it `service_account.json`

### Step 5: Get Backend URL

1. Go to the "Deployments" tab
2. Copy the URL (e.g., `https://calendar-ai-backend-production.up.railway.app`)
3. Test it by visiting `/health` endpoint

### Step 6: Deploy Frontend

```bash
cd ../frontend
railway init --name calendar-ai-frontend
railway variables set BACKEND_URL="YOUR_BACKEND_URL_HERE"
railway up
```

Replace `YOUR_BACKEND_URL_HERE` with the URL from Step 5.

### Step 7: Get Frontend URL

1. Go to your `calendar-ai-frontend` project in Railway dashboard
2. Copy the frontend URL
3. Test your application!

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend won't start
**Solution**: 
- Check environment variables are set correctly
- Verify `service_account.json` is uploaded
- Check Railway logs for error messages

**Problem**: LLM API errors
**Solution**:
- Verify API keys are correct
- Check API provider status
- Review Railway logs

### Frontend Issues

**Problem**: Frontend can't connect to backend
**Solution**:
- Verify `BACKEND_URL` environment variable is set correctly
- Check backend is running and healthy
- Test backend URL directly

### Google Calendar Issues

**Problem**: Calendar integration not working
**Solution**:
- Verify service account has correct permissions
- Check calendar is shared with service account email
- Verify Calendar API is enabled

## 📊 Monitoring

### Health Checks

- **Backend Health**: `https://your-backend-url.railway.app/health`
- **Frontend**: `https://your-frontend-url.railway.app/`

### Railway Dashboard

Monitor your applications at: https://railway.app/dashboard

## 🎉 Success!

Once deployed, you'll have:
- ✅ **Backend URL**: `https://your-backend-url.railway.app`
- ✅ **Frontend URL**: `https://your-frontend-url.railway.app`
- ✅ **Working Calendar AI Assistant** ready for testing!

## 📞 Need Help?

1. **Railway Documentation**: https://docs.railway.app/
2. **Railway Community**: https://community.railway.app/
3. **Project Issues**: Open an issue in the repository

---

**Your Calendar AI Assistant is now live and ready for the world! 🌍** 