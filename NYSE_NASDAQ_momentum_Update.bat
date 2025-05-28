@echo off
echo [%date% %time%] バッチ呼び出し >> task_debug.log

cd /d C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Users\tonoma\AppData\Local\Programs\Python\Python313\python.exe" momentum_calculator.py >> momentum_log.txt 2>&1

echo [%date% %time%] バッチ終了 code=%ERRORLEVEL% >> task_debug.log



echo yfinanceデータ取得開始
C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\Mom_US\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
echo データ取得完了

echo git push開始
cd C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Update commit"
"C:\Program Files\Git\cmd\git.exe" push -u origin_momentum_nyse_nasdaq main
echo git push完了

echo 現在日時取得
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




