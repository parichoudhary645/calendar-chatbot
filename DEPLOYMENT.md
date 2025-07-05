# 🚀 Deployment Guide

This guide will help you deploy your Calendar Booking Chatbot to various platforms.

## 📋 Prerequisites

Before deploying, make sure you have:
1. ✅ OpenAI API key
2. ✅ Google Service Account JSON file
3. ✅ Calendar shared with service account
4. ✅ All code committed to Git repository

## 🎯 Platform Options

### Option 1: Railway (Recommended - Easiest)

Railway is the easiest platform for deployment with automatic scaling and easy environment variable management.

#### Backend Deployment

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy Backend**:
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Set Environment Variables** in Railway Dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SERVICE_ACCOUNT_FILE`: Upload your `service_account.json` file

5. **Get Backend URL**: Copy the URL from Railway dashboard (e.g., `https://your-app.railway.app`)

#### Frontend Deployment

1. **Update Backend URL** in `frontend/app.py`:
   ```python
   BACKEND_URL = "https://your-backend-url.railway.app"
   ```

2. **Deploy Frontend**:
   ```bash
   cd frontend
   railway init
   railway up
   ```

3. **Get Frontend URL**: Copy the URL from Railway dashboard

### Option 2: Render

Render offers free hosting with automatic deployments from Git.

#### Backend Deployment

1. **Create New Web Service** on Render
2. **Connect your Git repository**
3. **Configure**:
   - **Name**: `calendar-chatbot-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - Add `service_account.json` as a file in the dashboard

5. **Deploy** and get your backend URL

#### Frontend Deployment

1. **Create New Web Service** on Render
2. **Configure**:
   - **Name**: `calendar-chatbot-frontend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Update Backend URL** in `frontend/app.py`
4. **Deploy**

### Option 3: Fly.io

Fly.io offers global deployment with Docker containers.

#### Create Dockerfiles

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

#### Deploy

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly**:
   ```bash
   fly auth login
   ```

3. **Deploy Backend**:
   ```bash
   cd backend
   fly launch
   fly secrets set OPENAI_API_KEY=your_key_here
   fly deploy
   ```

4. **Deploy Frontend**:
   ```bash
   cd frontend
   fly launch
   fly deploy
   ```

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `SERVICE_ACCOUNT_FILE` | Path to Google service account JSON | `service_account.json` |

### Platform-Specific Setup

#### Railway
- Go to your project dashboard
- Click "Variables" tab
- Add each variable with its value
- Upload `service_account.json` as a file

#### Render
- Go to your service dashboard
- Click "Environment" tab
- Add each variable
- Upload `service_account.json` in the "Files" section

#### Fly.io
```bash
fly secrets set OPENAI_API_KEY=your_key_here
# Upload service_account.json to the app
```

## 🌐 Domain Configuration

### Custom Domain (Optional)

1. **Railway**: Go to Settings > Domains
2. **Render**: Go to Settings > Custom Domains
3. **Fly.io**: `fly certs add yourdomain.com`

### SSL/HTTPS

All platforms provide automatic SSL certificates.

## 📊 Monitoring

### Health Checks

Your backend includes a health check endpoint:
- URL: `https://your-backend-url/health`
- Returns: `{"status": "healthy", "agent_ready": true}`

### Logs

- **Railway**: `railway logs`
- **Render**: Dashboard > Logs tab
- **Fly.io**: `fly logs`

## 🔄 Continuous Deployment

### Automatic Deployments

All platforms support automatic deployments from Git:
1. Connect your GitHub repository
2. Push changes to trigger deployment
3. Monitor deployment status

### Manual Deployments

```bash
# Railway
railway up

# Render
# Automatic from Git

# Fly.io
fly deploy
```

## 🐛 Troubleshooting

### Common Deployment Issues

1. **Build Failures**:
   - Check requirements.txt syntax
   - Verify Python version compatibility
   - Check for missing dependencies

2. **Environment Variables**:
   - Verify all required variables are set
   - Check variable names (case-sensitive)
   - Ensure service account file is uploaded

3. **Connection Issues**:
   - Verify backend URL in frontend
   - Check CORS settings
   - Test backend health endpoint

4. **Calendar Access**:
   - Ensure service account has calendar permissions
   - Verify calendar is shared with service account email
   - Check Google Cloud project settings

### Debug Commands

```bash
# Check backend health
curl https://your-backend-url/health

# Test API endpoint
curl -X POST https://your-backend-url/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# View logs
railway logs  # or platform-specific command
```

## 📈 Scaling

### Automatic Scaling

- **Railway**: Automatic based on traffic
- **Render**: Manual scaling in dashboard
- **Fly.io**: `fly scale count 2`

### Performance Optimization

1. **Caching**: Implement Redis for session storage
2. **Database**: Add PostgreSQL for conversation history
3. **CDN**: Use Cloudflare for static assets

## 🔒 Security

### Best Practices

1. **Environment Variables**: Never commit secrets to Git
2. **API Keys**: Rotate keys regularly
3. **Service Account**: Use minimal required permissions
4. **HTTPS**: Always use HTTPS in production

### Security Headers

Add security headers to your FastAPI app:
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
```

## 📞 Support

### Platform Support

- **Railway**: [Discord](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Fly.io**: [Community](https://community.fly.io)

### Project Issues

For project-specific issues, check:
1. README.md troubleshooting section
2. GitHub issues
3. Stack Overflow

---

**Happy Deploying! 🚀** 