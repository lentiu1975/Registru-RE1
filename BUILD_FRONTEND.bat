@echo off
REM Script pentru build frontend React

echo ============================================
echo Building React Frontend pentru Productie
echo ============================================
echo.

cd frontend

echo Creez fisier .env.production...
echo REACT_APP_API_URL=https://vama.lentiu.ro/api > .env.production

echo.
echo Rulez npm install...
call npm install

echo.
echo Rulez npm build...
call npm run build

echo.
echo ============================================
echo Build finalizat!
echo ============================================
echo.
echo Directorul frontend/build/ este gata pentru upload.
echo Upload continutul din frontend/build/ pe server la:
echo   /home/lentiuro/public_html/
echo.
pause
