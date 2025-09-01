#!/bin/bash

echo "🚀 Quick Netlify Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install Node.js first."
    exit 1
fi

# Navigate to frontend
cd frontend

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building production version..."
npm run build

echo "✅ Build complete!"
echo ""
echo "🌐 Next Steps for Netlify Deployment:"
echo "1. Go to https://netlify.com and sign up/login"
echo "2. Drag and drop the 'frontend/build' folder to deploy"
echo "3. Or connect your GitHub repository for automatic deployments"
echo ""
echo "📁 Build folder location: $(pwd)/build"
echo "🔗 Your frontend will be available at: https://[random-name].netlify.app"
echo ""
echo "💡 For custom domain: Go to Site Settings → Domain Management in Netlify"
