# 🚀 Deployment Checklist

Use this checklist to ensure your Calendar AI Assistant is properly deployed and working.

## 📋 Pre-Deployment Checklist

### ✅ Prerequisites
- [ ] Railway account created at [railway.app](https://railway.app)
- [ ] Git repository with all code committed
- [ ] API keys ready:
  - [ ] `GROQ_API_KEY` (Primary LLM)
  - [ ] `GOOGLE_API_KEY` (Gemini fallback)
  - [ ] `OPENAI_API_KEY` (Optional)
  - [ ] `ANTHROPIC_API_KEY` (Optional)
- [ ] Google Service Account JSON file (`service_account.json`)
- [ ] Google Calendar shared with service account email

### ✅ Local Testing
- [ ] Backend runs locally (`cd backend && python main.py`)
- [ ] Frontend runs locally (`cd frontend && streamlit run app.py`)
- [ ] Booking functionality works
- [ ] Schedule queries work
- [ ] Calendar integration works

## 🔧 Deployment Steps

### Step 1: Create Render Account
- [ ] Sign up at [render.com](https://render.com)
- [ ] Verify email address

### Step 2: Deploy Backend
- [ ] Go to Render Dashboard → "New +" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Configure:
  - Name: `calendar-ai-backend`
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python main.py`
- [ ] Click "Create Web Service"

### Step 3: Configure Backend Environment Variables
In Render Dashboard → calendar-ai-backend → Environment:

- [ ] `GROQ_API_KEY` = your_groq_api_key_here
- [ ] `GOOGLE_API_KEY` = your_gemini_api_key_here
- [ ] `OPENAI_API_KEY` = your_openai_api_key_here (optional)
- [ ] `ANTHROPIC_API_KEY` = your_anthropic_api_key_here (optional)
- [ ] `SERVICE_ACCOUNT_JSON` = entire content of service_account.json file

### Step 4: Get Backend URL
- [ ] Wait for deployment to complete
- [ ] Copy the URL (e.g., `https://calendar-ai-backend.onrender.com`)

### Step 5: Deploy Frontend
- [ ] Go to Render Dashboard → "New +" → "Web Service"
- [ ] Connect the same GitHub repository
- [ ] Configure:
  - Name: `calendar-ai-frontend`
  - Root Directory: `frontend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Click "Create Web Service"

### Step 6: Configure Frontend Environment Variables
In Render Dashboard → calendar-ai-frontend → Environment:

- [ ] `BACKEND_URL` = your_backend_url_from_step_4

## 🧪 Post-Deployment Testing

### ✅ Backend Testing
- [ ] Health check: `https://your-backend-url/health`
- [ ] Chat endpoint: `https://your-backend-url/chat`
- [ ] Backend logs show no errors

### ✅ Frontend Testing
- [ ] Frontend loads at Railway URL
- [ ] Chat interface is responsive
- [ ] Can send messages
- [ ] Receives responses from backend

### ✅ Functionality Testing
- [ ] **Booking Test**: "Book a meeting tomorrow at 3pm called Test Meeting"
- [ ] **Schedule Test**: "What's my schedule today?"
- [ ] **Availability Test**: "Is 2pm tomorrow available?"
- [ ] **Calendar Integration**: Events appear in Google Calendar

## 🔍 Troubleshooting Checklist

### Backend Issues
- [ ] Check Render logs: Go to service → Logs tab
- [ ] Verify environment variables are set correctly
- [ ] Check `SERVICE_ACCOUNT_JSON` contains valid JSON
- [ ] Verify API keys are valid and have credits

### Frontend Issues
- [ ] Check Render logs: Go to service → Logs tab
- [ ] Verify `BACKEND_URL` is set correctly
- [ ] Test backend health endpoint manually
- [ ] Check CORS configuration

### Calendar Integration Issues
- [ ] Verify service account JSON is uploaded correctly
- [ ] Check calendar is shared with service account email
- [ ] Test with simple calendar operations
- [ ] Check Google Calendar API quotas

## 📊 Monitoring Checklist

### Railway Dashboard
- [ ] Both services are running (green status)
- [ ] No error logs in recent deployments
- [ ] Resource usage is reasonable
- [ ] Environment variables are set correctly

### Application Health
- [ ] Backend health endpoint returns 200
- [ ] Frontend loads without errors
- [ ] Chat functionality works
- [ ] Calendar operations succeed

## 🎯 Final Verification

### ✅ Production Readiness
- [ ] All tests pass
- [ ] No sensitive data exposed
- [ ] Error handling works
- [ ] Performance is acceptable
- [ ] SSL/HTTPS is enabled

### ✅ Documentation
- [ ] Update README with production URLs
- [ ] Document any custom configurations
- [ ] Note any platform-specific settings
- [ ] Share deployment guide with team

## 🚀 Success Criteria

Your deployment is successful when:

1. **Frontend URL**: Accessible and functional
2. **Backend URL**: Health check passes
3. **Booking**: Can create real calendar events
4. **Schedule**: Can query real calendar data
5. **Availability**: Can check real calendar availability
6. **LLM**: AI responses are working
7. **Integration**: All components work together

## 📞 Support Resources

- [Render Documentation](https://render.com/docs)
- [Render Status](https://status.render.com)
- [Project Documentation](PROJECT_SUMMARY.md)
- [Deployment Guide](RENDER_DEPLOYMENT.md)

---

**🎉 Congratulations! Your Calendar AI Assistant is now live and ready for production use!** 