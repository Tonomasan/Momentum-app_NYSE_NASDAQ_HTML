echo yfinanceデータ取得開始
C:\Users\tonoma\.virtualenvs\kabu-ySnafzVC\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ\momentum_calculator.py
timeout /t 7000 /nobreak
echo データ取得完了

echo git push開始
cd C:\work\kabu\Momentum_NYSE_NASDAQ
git add .
git commit -m "Update commit"
git push -u origin_momentum_nyse_nasdaq main
echo git push完了
pause
