@echo off
echo [%date% %time%] �o�b�`�Ăяo�� >> task_debug.log

cd /d C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Users\tonoma\AppData\Local\Programs\Python\Python313\python.exe" momentum_calculator.py >> momentum_log.txt 2>&1

echo [%date% %time%] �o�b�`�I�� code=%ERRORLEVEL% >> task_debug.log



echo yfinance�f�[�^�擾�J�n
C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\Mom_US\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
echo �f�[�^�擾����

echo git push�J�n
cd C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Update commit"
"C:\Program Files\Git\cmd\git.exe" push -u origin_momentum_nyse_nasdaq main
echo git push����

echo ���ݓ����擾
cd /d %~dp0
setlocal enabledelayedexpansion
set YYYY=%Date:~0,4%
set MM=%Date:~5,2%
set DD=%Date:~8,2%
set HH=%Time:~0,2%
set HH=%HH: =0%
set MIN=%Time:~3,2%
set MIN=%MIN: =0%
set SS=%Time:~6,2%
set SS=%SS: =0%
set TIMESTAMP=%YYYY%/%MM%/%DD%/%HH%%MIN%
echo Time = %TIMESTAMP%
endlocal

pause




