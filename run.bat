@echo off
echo Installing/Updating required packages...
pip install -r requirements.txt
echo.
echo Starting Auto Paste Typer...
python paste_typer.py
pause

