@echo off
echo yfinance�f�[�^�擾�J�n
C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\Mom_US\Scripts\python.exe C:\work\kabu\Momentum_NYSE_NASDAQ_HTML\momentum_calculator.py
echo �f�[�^�擾����

echo git push�J�n
cd C:\work\kabu\Momentum_NYSE_NASDAQ_HTML
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Update commit"
"C:\Program Files\Git\cmd\git.exe" push -u origin_momentum_nyse_nasdaq main
echo git push����

pause



