@echo off
echo 🚀 Quick Netlify Deployment Script for Windows
echo ==============================================

REM Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: npm is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Navigate to frontend
cd frontend

echo 📦 Installing dependencies...
npm install

echo 🔨 Building production version...
npm run build

echo ✅ Build complete!
echo.
echo 🌐 Next Steps for Netlify Deployment:
echo 1. Go to https://netlify.com and sign up/login
echo 2. Drag and drop the 'frontend/build' folder to deploy
echo 3. Or connect your GitHub repository for automatic deployments
echo.
echo 📁 Build folder location: %cd%\build
echo 🔗 Your frontend will be available at: https://[random-name].netlify.app
echo.
echo 💡 For custom domain: Go to Site Settings → Domain Management in Netlify
echo.
pause
