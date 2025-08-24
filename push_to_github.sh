#!/bin/bash

echo "📦 Creating GitHub repository..."
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: forward-horizon-api"
echo "3. Make it Public"
echo "4. DON'T initialize with README (we already have one)"
echo "5. Click 'Create repository'"
echo ""
echo "Once created, copy the repository URL (like: https://github.com/YOUR_USERNAME/forward-horizon-api.git)"
echo ""
read -p "Paste your repository URL here: " REPO_URL

# Add remote and push
git remote remove origin 2>/dev/null || true
git remote add origin $REPO_URL
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "Now go to Railway:"
echo "1. Visit: https://railway.app/new"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Select 'forward-horizon-api'"
echo "4. Railway will start deploying automatically!"