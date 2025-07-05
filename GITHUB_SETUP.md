# 🚀 GitHub Repository Setup Guide

This guide will help you create a GitHub repository and push your Calendar AI Assistant code for easy deployment.

## 📋 Prerequisites

1. ✅ **GitHub Account**: Sign up at [github.com](https://github.com)
2. ✅ **Git installed**: Already installed on your system
3. ✅ **Code ready**: Your project is already committed locally

## 🔧 Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub**: [github.com](https://github.com)
2. **Click "New repository"** (green button)
3. **Configure repository**:
   - **Repository name**: `calendar-ai-assistant` (or your preferred name)
   - **Description**: `A production-ready conversational AI assistant for Google Calendar management`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. **Click "Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/calendar-ai-assistant.git

# Set the main branch (if not already set)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Step 3: Verify Repository

1. **Go to your repository URL**: `https://github.com/YOUR_USERNAME/calendar-ai-assistant`
2. **Verify all files are there**:
   - ✅ Backend code (`backend/` folder)
   - ✅ Frontend code (`frontend/` folder)
   - ✅ Deployment guides
   - ✅ Documentation files
   - ✅ Configuration files

## 🔐 Security Considerations

### Files NOT in Repository (Protected by .gitignore)

- ✅ `service_account.json` - Your real Google service account
- ✅ `.env` files - Environment variables with API keys
- ✅ `__pycache__/` - Python cache files
- ✅ IDE files (`.vscode/`, `.idea/`)

### Files in Repository (Safe to Share)

- ✅ `service_account.json.example` - Template file
- ✅ `env.example` - Environment variable template
- ✅ All source code
- ✅ Deployment guides
- ✅ Documentation

## 🚀 Deployment Ready

Once your code is on GitHub, you can easily deploy to any platform:

### Railway Deployment
```bash
# Railway will automatically detect your GitHub repository
# Just connect it in the Railway dashboard
```

### Render Deployment
```bash
# Render will automatically detect your GitHub repository
# Just connect it in the Render dashboard
```

### Fly.io Deployment
```bash
# Fly.io will automatically detect your GitHub repository
# Just connect it in the Fly.io dashboard
```

## 📝 Repository Structure

Your GitHub repository will have this structure:

```
calendar-ai-assistant/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── simple_llm_agent.py     # AI agent with LLM integration
│   ├── calendar_utils.py       # Google Calendar API wrapper
│   ├── requirements.txt        # Backend dependencies
│   ├── Procfile               # Railway deployment config
│   └── service_account.json.example  # Template file
├── frontend/
│   ├── app.py                  # Streamlit interface
│   ├── requirements.txt        # Frontend dependencies
│   └── Procfile               # Railway deployment config
├── README.md                   # Project overview
├── PROJECT_SUMMARY.md          # Technical documentation
├── DEPLOYMENT.md              # General deployment guide
├── RAILWAY_DEPLOYMENT.md      # Railway-specific guide
├── RENDER_DEPLOYMENT.md       # Render-specific guide
├── FLY_DEPLOYMENT.md          # Fly.io-specific guide
├── DEPLOYMENT_CHECKLIST.md    # Deployment checklist
├── .gitignore                 # Git ignore rules
├── railway.json               # Railway configuration
├── deploy.sh                  # Deployment script
└── test_deployment.py         # Deployment testing script
```

## 🔄 Continuous Deployment

Once connected to GitHub, most platforms support automatic deployments:

- **Railway**: Deploys on every push to main branch
- **Render**: Deploys on every push to main branch
- **Fly.io**: Deploys on every push to main branch

## 🎯 Next Steps After GitHub Setup

1. **Choose your deployment platform**:
   - Railway (if you upgrade to Pro)
   - Render (recommended for free tier)
   - Fly.io (good free tier)

2. **Follow the platform-specific guide**:
   - `RAILWAY_DEPLOYMENT.md`
   - `RENDER_DEPLOYMENT.md`
   - `FLY_DEPLOYMENT.md`

3. **Set up environment variables** in your chosen platform

4. **Test your deployment**

## 🔍 Troubleshooting

### Common Issues

#### 1. Repository Already Exists
```bash
# If you get "repository already exists" error
git remote set-url origin https://github.com/YOUR_USERNAME/calendar-ai-assistant.git
```

#### 2. Authentication Issues
```bash
# Use GitHub CLI for easier authentication
brew install gh  # macOS
gh auth login
```

#### 3. Large Files
```bash
# If you have large files that shouldn't be in Git
git rm --cached large_file.txt
git commit -m "Remove large file"
```

### Verification Commands

```bash
# Check remote repository
git remote -v

# Check branch
git branch

# Check status
git status

# View commit history
git log --oneline
```

## 🎉 Success Checklist

- ✅ GitHub repository created
- ✅ Local repository connected to GitHub
- ✅ All code pushed to GitHub
- ✅ Sensitive files protected (.gitignore working)
- ✅ Repository structure is correct
- ✅ Ready for deployment

Your project is now ready for easy deployment from GitHub! 🚀 