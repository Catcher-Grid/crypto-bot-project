@echo off
title Crypto Grid Bot - RUNNING
echo Запуск Telegram-команд...
start cmd /k "python modules\telegram_commands.py"
timeout /t 3 > nul
echo Запуск основного бота...
python modules\main.py
pause