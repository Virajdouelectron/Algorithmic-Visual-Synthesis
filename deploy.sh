#!/bin/bash
# Deployment Script for Algorithmic Visual Synthesis
# Usage: ./deploy.sh [platform]

set -e

PLATFORM=${1:-"help"}

echo "🚀 Algorithmic Visual Synthesis - Deployment Script"
echo "=================================================="

case $PLATFORM in
  "github")
    echo "📦 Deploying to GitHub Pages..."
    echo ""
    echo "Steps:"
    echo "1. Make sure you're in the project directory"
    echo "2. Initialize git if not already: git init"
    echo "3. Add all files: git add ."
    echo "4. Commit: git commit -m 'Deploy to GitHub Pages'"
    echo "5. Push to GitHub: git push origin main"
    echo "6. Enable GitHub Pages in repository settings"
    echo ""
    echo "Your site will be available at:"
    echo "https://yourusername.github.io/algorithmic-visual-synthesis/"
    ;;
    
  "netlify")
    echo "🌐 Deploying to Netlify..."
    if command -v netlify &> /dev/null; then
      netlify deploy --prod
    else
      echo "Netlify CLI not installed. Install with: npm install -g netlify-cli"
      echo ""
      echo "Or deploy via Netlify Dashboard:"
      echo "1. Go to https://netlify.com"
      echo "2. Drag and drop this folder"
      echo "3. Your site will be live!"
    fi
    ;;
    
  "vercel")
    echo "▲ Deploying to Vercel..."
    if command -v vercel &> /dev/null; then
      vercel --prod
    else
      echo "Vercel CLI not installed. Install with: npm install -g vercel"
      echo ""
      echo "Or deploy via Vercel Dashboard:"
      echo "1. Go to https://vercel.com"
      echo "2. Import your Git repository"
      echo "3. Deploy!"
    fi
    ;;
    
  "surge")
    echo "📡 Deploying to Surge..."
    if command -v surge &> /dev/null; then
      surge
    else
      echo "Surge not installed. Install with: npm install -g surge"
    fi
    ;;
    
  "local")
    echo "🏠 Starting local server..."
    if command -v python3 &> /dev/null; then
      echo "Starting Python HTTP server on http://localhost:8000"
      python3 -m http.server 8000
    elif command -v python &> /dev/null; then
      echo "Starting Python HTTP server on http://localhost:8000"
      python -m http.server 8000
    else
      echo "Python not found. Please install Python 3"
    fi
    ;;
    
  "check")
    echo "✅ Checking deployment readiness..."
    echo ""
    
    # Check required files
    REQUIRED_FILES=("gallery.html" "gallery.css" "gallery.js")
    MISSING_FILES=()
    
    for file in "${REQUIRED_FILES[@]}"; do
      if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
      fi
    done
    
    if [ ${#MISSING_FILES[@]} -eq 0 ]; then
      echo "✅ All required files present"
    else
      echo "❌ Missing files:"
      for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
      done
      exit 1
    fi
    
    # Check file sizes
    echo ""
    echo "📊 File sizes:"
    for file in "${REQUIRED_FILES[@]}"; do
      if [ -f "$file" ]; then
        size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "unknown")
        echo "   - $file: $size"
      fi
    done
    
    echo ""
    echo "✅ Ready for deployment!"
    ;;
    
  "help"|*)
    echo "Usage: ./deploy.sh [platform]"
    echo ""
    echo "Platforms:"
    echo "  github  - Deploy to GitHub Pages"
    echo "  netlify - Deploy to Netlify"
    echo "  vercel  - Deploy to Vercel"
    echo "  surge   - Deploy to Surge.sh"
    echo "  local   - Start local development server"
    echo "  check   - Check deployment readiness"
    echo "  help    - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh github"
    echo "  ./deploy.sh netlify"
    echo "  ./deploy.sh check"
    ;;
esac

