REM git push開始
cd /d C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Update commit"
"C:\Program Files\Git\cmd\git.exe" push -u origin_momentum_nyse_nasdaq main

REM git push完了
pause

REM yfinanceデータ取得開始
C:\Users\tonoma\.virtualenvs\kabu-ySnafzVC\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
REM データ取得完了


