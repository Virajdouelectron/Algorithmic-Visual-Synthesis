@echo off
REM Deployment Script for Algorithmic Visual Synthesis (Windows)
REM Usage: deploy.bat [platform]

set PLATFORM=%1
if "%PLATFORM%"=="" set PLATFORM=help

echo.
echo ================================================
echo   Algorithmic Visual Synthesis - Deployment
echo ================================================
echo.

if "%PLATFORM%"=="github" goto github
if "%PLATFORM%"=="netlify" goto netlify
if "%PLATFORM%"=="vercel" goto vercel
if "%PLATFORM%"=="surge" goto surge
if "%PLATFORM%"=="local" goto local
if "%PLATFORM%"=="check" goto check
goto help

:github
echo Deploying to GitHub Pages...
echo.
echo Steps:
echo 1. Make sure you're in the project directory
echo 2. Initialize git if not already: git init
echo 3. Add all files: git add .
echo 4. Commit: git commit -m "Deploy to GitHub Pages"
echo 5. Push to GitHub: git push origin main
echo 6. Enable GitHub Pages in repository settings
echo.
echo Your site will be available at:
echo https://yourusername.github.io/algorithmic-visual-synthesis/
goto end

:netlify
echo Deploying to Netlify...
where netlify >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    netlify deploy --prod
) else (
    echo Netlify CLI not installed. Install with: npm install -g netlify-cli
    echo.
    echo Or deploy via Netlify Dashboard:
    echo 1. Go to https://netlify.com
    echo 2. Drag and drop this folder
    echo 3. Your site will be live!
)
goto end

:vercel
echo Deploying to Vercel...
where vercel >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    vercel --prod
) else (
    echo Vercel CLI not installed. Install with: npm install -g vercel
    echo.
    echo Or deploy via Vercel Dashboard:
    echo 1. Go to https://vercel.com
    echo 2. Import your Git repository
    echo 3. Deploy!
)
goto end

:surge
echo Deploying to Surge...
where surge >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    surge
) else (
    echo Surge not installed. Install with: npm install -g surge
)
goto end

:local
echo Starting local server...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Starting Python HTTP server on http://localhost:8000
    python -m http.server 8000
) else (
    echo Python not found. Please install Python 3
)
goto end

:check
echo Checking deployment readiness...
echo.
if exist gallery.html (
    echo [OK] gallery.html found
) else (
    echo [ERROR] gallery.html missing
)
if exist gallery.css (
    echo [OK] gallery.css found
) else (
    echo [ERROR] gallery.css missing
)
if exist gallery.js (
    echo [OK] gallery.js found
) else (
    echo [ERROR] gallery.js missing
)
echo.
echo Ready for deployment!
goto end

:help
echo Usage: deploy.bat [platform]
echo.
echo Platforms:
echo   github  - Deploy to GitHub Pages
echo   netlify - Deploy to Netlify
echo   vercel  - Deploy to Vercel
echo   surge   - Deploy to Surge.sh
echo   local   - Start local development server
echo   check   - Check deployment readiness
echo   help    - Show this help message
echo.
echo Examples:
echo   deploy.bat github
echo   deploy.bat netlify
echo   deploy.bat check

:end
pause

