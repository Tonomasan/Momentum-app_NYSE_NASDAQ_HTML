rem @echo off
rem echo yfinanceデータ取得開始
rem C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\Mom_US\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
rem echo データ取得完了

echo git push開始
cd /d C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Update commit"
"C:\Program Files\Git\cmd\git.exe" push -u origin_momentum_nyse_nasdaq main
echo git push完了

pause



