@echo off
chcp 65001 >nul
cd C:\Users\Вика\Desktop\ПАК
C:\Users\Вика\AppData\Local\Programs\Python\Python313\python.exe -m uvicorn veb:app --reload --host 127.0.0.1 --port 8000
pause