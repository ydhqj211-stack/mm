@echo off
echo ========================================
echo   SMS Watcher - Push to GitHub
echo ========================================
echo.

cd /d "%~dp0.."

echo Checking git status...
git status

echo.
echo ========================================
echo Instructions:
echo 1. Make sure you have committed your changes
echo 2. Add your GitHub remote:
echo    git remote add origin https://github.com/ydhqj211-stack/mm.git
echo 3. Push to GitHub:
echo    git push -u origin main
echo ========================================
echo.

set /p confirm="Press Enter to open GitHub repository in browser, or Ctrl+C to cancel..."
start https://github.com/ydhqj211-stack/mm