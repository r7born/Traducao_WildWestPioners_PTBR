@echo off
chcp 65001 >nul
cd /d "%~dp0"
python aplicar_traducao.py --restaurar
pause
