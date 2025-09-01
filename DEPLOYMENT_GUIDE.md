# 🚀 Deployment Guide: Police Financial Crime Investigation System

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment (AWS/Azure)](#cloud-deployment)
6. [Police Station Setup](#police-station-setup)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### **System Requirements**
- **Operating System**: Windows 10/11, Ubuntu 18+, macOS 10.15+
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: 5GB free space
- **Internet**: Required for initial setup and optional banking APIs

### **Software Dependencies**
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

---

## 💻 Local Development Setup

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions.git
cd AI-Model-for-Flagging-Suspicious-Transactions
```

### **Step 2: Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create ML model files (if not present)
cd app/model
python train_model.py  # Creates the model files

# Return to backend directory
cd ../..

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### **Step 3: Frontend Setup**
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

### **Step 4: Verify Deployment**
- **Backend API**: Open http://localhost:8001/docs
- **Frontend Dashboard**: Open http://localhost:3000
- **Health Check**: Visit http://localhost:8001/ for API status

---

## 🏭 Production Deployment

### **Step 1: Prepare Production Environment**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
sudo apt install python3 python3-pip nodejs npm -y

# Install process manager
sudo npm install -g pm2
```

### **Step 2: Deploy Backend**
```bash
# Clone repository
git clone <your-repo-url>
cd AI-Model-for-Flagging-Suspicious-Transactions/backend

# Create production virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn

# Create gunicorn configuration
cat > gunicorn.conf.py << EOF
bind = "0.0.0.0:8001"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
EOF

# Start production server
gunicorn app.main:app -c gunicorn.conf.py --daemon
```

### **Step 3: Deploy Frontend**
```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Build production version
npm run build

# Install serve globally
sudo npm install -g serve

# Start production frontend
serve -s build -l 3000 &
```

### **Step 4: Setup Reverse Proxy (Nginx)**
```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo cat > /etc/nginx/sites-available/fraud-detection << EOF
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/fraud-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🐳 Docker Deployment

### **Step 1: Create Dockerfiles**

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

EXPOSE 3000
```

### **Step 2: Create Docker Compose**

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./backend/app/model:/app/app/model
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

### **Step 3: Deploy with Docker**
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## ☁️ Cloud Deployment (AWS/Azure)

### **AWS Deployment**

**Step 1: Setup EC2 Instance**
```bash
# Launch EC2 instance (t3.medium recommended)
# Security Group: Allow ports 22, 80, 443, 3000, 8001

# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
```

**Step 2: Deploy Application**
```bash
# Clone repository
git clone <your-repo>
cd AI-Model-for-Flagging-Suspicious-Transactions

# Deploy with Docker Compose
docker-compose up -d

# Setup domain (optional)
# Point your domain to EC2 public IP
```

### **Azure Deployment**

**Step 1: Azure Container Instances**
```bash
# Create resource group
az group create --name fraud-detection-rg --location eastus

# Create container group
az container create \
  --resource-group fraud-detection-rg \
  --name fraud-detection-app \
  --image your-registry/fraud-detection:latest \
  --ports 80 443 \
  --dns-name-label fraud-detection-unique
```

---

## 🌐 Easy Deployment: Netlify & Vercel

### **🚀 Netlify Deployment (Frontend Only)**

**Prerequisites:**
- GitHub account with your repository
- Netlify account (free tier available)

**Step 1: Prepare Your Frontend**
```bash
# Navigate to frontend directory
cd frontend

# Create production build script in package.json
# Ensure this exists in your package.json:
{
  "scripts": {
    "build": "react-scripts build",
    "start": "react-scripts start"
  }
}

# Create netlify configuration
cat > netlify.toml << EOF
[build]
  publish = "build"
  command = "npm run build"

[build.environment]
  REACT_APP_API_URL = "https://your-backend-url.herokuapp.com"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
```

**Step 2: Deploy on Netlify**
1. **Login to Netlify**: Go to [netlify.com](https://netlify.com) and sign up/login
2. **Connect GitHub**: Click "New site from Git" → "GitHub"
3. **Select Repository**: Choose `AI-Model-for-Flagging-Suspicious-Transactions`
4. **Configure Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
5. **Environment Variables**: Add in Site Settings → Environment Variables:
   ```
   REACT_APP_API_URL = https://your-backend-url.com
   ```
6. **Deploy**: Click "Deploy site"

**Step 3: Custom Domain (Optional)**
```bash
# In Netlify dashboard:
1. Go to Site Settings → Domain Management
2. Add custom domain
3. Configure DNS records as shown
4. Enable HTTPS (automatic with Netlify)
```

### **⚡ Vercel Deployment (Frontend)**

**Step 1: Prepare Frontend for Vercel**
```bash
# Navigate to frontend
cd frontend

# Create vercel configuration
cat > vercel.json << EOF
{
  "name": "police-fraud-detection",
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "s-maxage=31536000,immutable"
      }
    },
    { "src": "/(.*)", "dest": "/" }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-backend-url.com"
  }
}
EOF
```

**Step 2: Deploy on Vercel**
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from Frontend Directory**:
   ```bash
   cd frontend
   vercel --prod
   ```

**Alternative: Vercel Dashboard Deployment**
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "New Project" → "Import Git Repository"
3. Select your GitHub repository
4. **Configure Project**:
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. **Environment Variables**:
   ```
   REACT_APP_API_URL = https://your-backend-url.com
   ```
6. Click "Deploy"

### **🔧 Backend Deployment Options for Netlify/Vercel**

Since Netlify and Vercel are primarily for frontend, here are backend options:

#### **Option 1: Heroku (Free Tier)**
```bash
# Install Heroku CLI
# Create Procfile in backend directory
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > backend/Procfile

# Deploy to Heroku
cd backend
git init
heroku create your-app-name
git add .
git commit -m "Deploy backend"
git push heroku main
```

#### **Option 2: Railway (Simple Backend Hosting)**
```bash
# Go to railway.app
# Connect GitHub repository
# Select backend folder
# Auto-deploys with zero configuration
```

#### **Option 3: Render (Free Backend Hosting)**
```bash
# Go to render.com
# Connect GitHub repository
# Create new Web Service
# Settings:
#   - Root Directory: backend
#   - Build Command: pip install -r requirements.txt
#   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **🎯 Complete Deployment Workflow**

**Step 1: Backend Deployment (Choose One)**
```bash
# Option A: Heroku
heroku create fraud-detection-api-2025
git subtree push --prefix=backend heroku main

# Option B: Railway
# Push to GitHub, connect to Railway, select backend folder

# Option C: Render
# Connect GitHub, configure as web service
```

**Step 2: Frontend Deployment**
```bash
# Update API URL in frontend/.env
REACT_APP_API_URL=https://your-backend-url.herokuapp.com

# Deploy to Netlify
netlify deploy --prod --dir=frontend/build

# OR Deploy to Vercel
cd frontend && vercel --prod
```

**Step 3: Test Complete System**
```bash
# Visit your deployed frontend URL
# Test transaction analysis
# Verify API connectivity
```

### **📱 One-Click Deployment Buttons**

Add these to your README.md for instant deployment:

```markdown
## Quick Deploy

### Frontend
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions&base=frontend)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions&project-name=fraud-detection&repository-name=fraud-detection&root-directory=frontend)

### Backend
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions/tree/main/backend)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions&envs=PORT&PORTDefault=8001)
```

### **💡 Pro Tips for Hackathon Demo**

1. **Live Demo URLs**: 
   - Frontend: `https://police-fraud-detection.netlify.app`
   - Backend: `https://fraud-api-2025.herokuapp.com`

2. **Quick Setup Commands**:
   ```bash
   # Clone and deploy in 2 minutes
   git clone https://github.com/SumantSagar73/AI-Model-for-Flagging-Suspicious-Transactions.git
   cd AI-Model-for-Flagging-Suspicious-Transactions
   ./deploy-netlify.sh  # Custom deployment script
   ```

3. **Demo Environment Variables**:
   ```bash
   REACT_APP_API_URL=https://fraud-api-demo.herokuapp.com
   REACT_APP_DEMO_MODE=true
   REACT_APP_SAMPLE_DATA=enabled
   ```

This gives you multiple deployment options with step-by-step guides perfect for your hackathon presentation! 🚀

---

## 🏛️ Police Station Setup

### **Minimal Police Station Requirements**
```bash
# Hardware Requirements
- Computer: Windows 10/11 with 4GB RAM
- Internet: 10 Mbps broadband connection
- Browser: Chrome, Firefox, or Edge (latest version)

# Software Installation (No technical skills required)
1. Download installer package
2. Run setup.exe
3. Follow guided installation
4. Access via desktop shortcut
```

### **Quick Police Station Deployment**
```bash
# Create installer package
# Package contents:
- portable-fraud-detection.exe (all-in-one executable)
- sample-data.csv (test transactions)
- user-manual.pdf (officer guide)
- quick-start.txt (5-minute setup)

# Installation steps for police IT staff:
1. Download fraud-detection-installer.zip
2. Extract to C:\FraudDetection\
3. Run start-system.bat
4. Open browser to http://localhost:3000
5. Upload sample data to test
```

### **Police Training Package**
```bash
# Training materials included:
- Video tutorial (15 minutes)
- Step-by-step guide with screenshots
- Common scenarios and solutions
- Troubleshooting FAQ
- Contact information for support
```

---

## 🔧 Environment Configuration

### **Backend Environment Variables**
Create `.env` file in backend directory:
```env
# API Configuration
FASTAPI_ENV=production
API_HOST=0.0.0.0
API_PORT=8001

# Model Configuration
MODEL_PATH=app/model/indian_banking_model.pkl
SCALER_PATH=app/model/indian_banking_scaler.pkl

# Banking API Configuration (Optional)
SBI_API_KEY=your_sbi_api_key
HDFC_API_KEY=your_hdfc_api_key
ICICI_API_KEY=your_icici_api_key

# Security
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

### **Frontend Environment Variables**
Create `.env` file in frontend directory:
```env
REACT_APP_API_URL=http://localhost:8001
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=2.0.0
```

---

## 🚀 Quick Start Commands

### **Development (Local Testing)**
```bash
# Terminal 1: Start Backend
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8001

# Terminal 2: Start Frontend  
cd frontend && npm install && npm start

# Access: http://localhost:3000
```

### **Production (One Command)**
```bash
# Using Docker Compose
docker-compose up -d

# Manual Production
./deploy-production.sh

# Police Station Setup
./install-police-station.bat
```

---

## 🔍 Health Checks and Monitoring

### **System Health Endpoints**
```bash
# Backend Health
curl http://localhost:8001/

# API Documentation
curl http://localhost:8001/docs

# Frontend Health
curl http://localhost:3000/

# Model Status
curl http://localhost:8001/model/status
```

### **Performance Monitoring**
```bash
# Check system resources
htop  # Linux
Task Manager  # Windows

# Check application logs
tail -f backend/logs/app.log

# Monitor API performance
curl -w "@curl-format.txt" http://localhost:8001/predict
```

---

## 🚨 Troubleshooting

### **Common Issues and Solutions**

#### **Backend Issues**
```bash
# Issue: Import errors
Solution: Check Python virtual environment activation
Fix: source venv/bin/activate (Linux) or venv\Scripts\activate (Windows)

# Issue: Model files not found
Solution: Ensure model files are in backend/app/model/
Fix: Run python train_model.py to generate models

# Issue: Port 8001 already in use
Solution: Change port or kill existing process
Fix: uvicorn app.main:app --port 8002
```

#### **Frontend Issues**
```bash
# Issue: npm install fails
Solution: Clear npm cache and retry
Fix: npm cache clean --force && npm install

# Issue: API connection error
Solution: Check backend is running and CORS settings
Fix: Verify REACT_APP_API_URL in .env file

# Issue: Build fails
Solution: Check Node.js version compatibility
Fix: Use Node.js 16.x or update package.json
```

#### **Deployment Issues**
```bash
# Issue: Docker build fails
Solution: Check Dockerfile syntax and base images
Fix: docker build --no-cache -t fraud-detection .

# Issue: Database connection errors
Solution: This system uses file-based models (no database required)
Fix: Ensure model files are accessible

# Issue: Permission denied
Solution: Check file permissions and ownership
Fix: sudo chown -R $USER:$USER /path/to/project
```

### **Support Contact**
- **Technical Issues**: Create GitHub issue with logs
- **Police Training**: Contact police.training@your-domain.com
- **Emergency Support**: Call +91-XXXX-XXXX-XX (24/7)

---

## 📈 Performance Optimization

### **Production Optimizations**
```bash
# Backend Optimizations
- Use gunicorn with multiple workers
- Enable gzip compression
- Implement caching for model predictions
- Use async/await for I/O operations

# Frontend Optimizations  
- Enable build optimizations (npm run build)
- Use CDN for static assets
- Implement lazy loading
- Enable browser caching

# Infrastructure Optimizations
- Use load balancer for high traffic
- Implement auto-scaling
- Set up monitoring and alerting
- Regular security updates
```

This deployment guide covers everything from local development to production deployment, making it easy for both developers and police IT staff to implement the system! 🎉
