REM git push開始
cd C:\work\kabu\Momentum_NYSE_NASDAQ
git add .
git commit -m "Update commit"
git push -u origin_momentum_nyse_nasdaq main
REM git push完了
pause
REM yfinanceデータ取得開始
C:\Users\tonoma\.virtualenvs\kabu-ySnafzVC\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
REM データ取得完了


