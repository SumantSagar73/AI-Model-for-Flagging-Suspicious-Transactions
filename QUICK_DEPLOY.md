# 🚀 Quick Deploy - Netlify & Vercel Guide

## 🎯 **Super Simple 3-Step Deployment**

### **📱 Option 1: Netlify (Drag & Drop - No Code Required!)**

**Step 1: Build Your App**
```bash
# Windows users - double click this file:
deploy-netlify.bat

# Mac/Linux users:
./deploy-netlify.sh
```

**Step 2: Deploy to Netlify**
1. Go to [netlify.com](https://netlify.com) 
2. Sign up with GitHub (free)
3. Drag the `frontend/build` folder to the deploy area
4. Done! Your app is live! 🎉

**Step 3: Get Your Live URL**
- Your app will be at: `https://amazing-name-123456.netlify.app`
- Share this URL for your hackathon demo!

---

### **⚡ Option 2: Vercel (One Command Deployment)**

**Step 1: Install & Deploy**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (will ask for login first time)
cd frontend
vercel --prod
```

**Step 2: Done!**
- Your app is live at: `https://your-app.vercel.app`
- Auto-deploys on every Git push!

---

## 🔧 **Backend Deployment (Choose One)**

### **🟢 Option A: Heroku (Recommended for Hackathons)**
```bash
# 1. Install Heroku CLI from heroku.com/cli
# 2. Login to Heroku
heroku login

# 3. Create app and deploy
cd backend
heroku create fraud-detection-api-2025
git init
git add .
git commit -m "Deploy backend"
git push heroku main

# 4. Your API is live at: https://fraud-detection-api-2025.herokuapp.com
```

### **🔵 Option B: Railway (Zero Configuration)**
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Deploy automatically! ✨

### **🟣 Option C: Render (Free Forever)**
1. Go to [render.com](https://render.com)
2. Connect GitHub → Create Web Service
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

---

## 🎪 **Complete Hackathon Setup (5 Minutes)**

### **The Fastest Way:**

```bash
# 1. Fork the repository on GitHub
# 2. Clone to your computer
git clone https://github.com/YOUR-USERNAME/AI-Model-for-Flagging-Suspicious-Transactions.git
cd AI-Model-for-Flagging-Suspicious-Transactions

# 3. Deploy frontend to Netlify
./deploy-netlify.bat  # Windows
./deploy-netlify.sh   # Mac/Linux

# 4. Deploy backend to Heroku
cd backend
heroku create your-app-name
git init && git add . && git commit -m "Deploy"
git push heroku main

# 5. Update frontend with backend URL
# Edit frontend/.env:
REACT_APP_API_URL=https://your-app-name.herokuapp.com

# 6. Redeploy frontend
cd ../frontend
npm run build
# Drag new build folder to Netlify
```

**Result:** Full-stack app live in 5 minutes! 🏆

---

## 📱 **One-Click Deploy Buttons**

Add these to your GitHub README for instant deployment:

**Frontend:**
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions&base=frontend)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions&root-directory=frontend)

**Backend:**
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions/tree/main/backend)

---

## 🎯 **Hackathon Demo URLs**

After deployment, you'll have:

- **Live Demo**: `https://police-fraud-detection.netlify.app`
- **API Docs**: `https://fraud-api-2025.herokuapp.com/docs`
- **GitHub**: `https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions`

Perfect for sharing with judges! 🏅

---

## 🚨 **Troubleshooting**

**Problem**: Build fails on Netlify
**Solution**: Check Node.js version in netlify.toml:
```toml
[build.environment]
  NODE_VERSION = "16"
```

**Problem**: API not connecting
**Solution**: Check CORS settings in backend and API URL in frontend

**Problem**: Heroku deployment fails
**Solution**: Ensure Procfile exists in backend folder

**Need Help?** Check the full DEPLOYMENT_GUIDE.md for detailed instructions!

---

**🎉 You're Ready for the Hackathon!** 
Your AI fraud detection system is now live and demo-ready! 🚀
