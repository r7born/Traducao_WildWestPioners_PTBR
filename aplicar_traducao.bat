@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul || (
    echo Python nao encontrado. Instale em https://www.python.org/downloads/ marcando "Add Python to PATH".
    pause
    exit /b 1
)
python aplicar_traducao.py
pause
