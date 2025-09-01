#!/bin/bash

echo "⚡ Quick Vercel Deployment Script"
echo "================================"

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

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Navigate to frontend
cd frontend

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building production version..."
npm run build

echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "🔗 Your app is now live on Vercel!"
echo "💡 You can manage your deployment at: https://vercel.com/dashboard"
