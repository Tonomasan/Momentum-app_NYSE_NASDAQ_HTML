import pandas as pd
import numpy as np
import time
import requests
import datetime
import yfinance as yf
import os
from pandas_datareader import data as pdr

# 📌 NYSE & NASDAQ 銘柄リストの GitHub URL
NYSE_URL = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nyse/nyse_tickers.txt"
NASDAQ_URL = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nasdaq/nasdaq_tickers.txt"

# ⏳ 過去何日間のモメンタムを計算するか設定
MOMENTUM_PERIODS = {
    "1w": 5,    # 1週間
    "1m": 21,   # 1か月
    "3m": 63,   # 3か月
    "6m": 126,  # 6か月
    "1y": 252   # 1年
}

# 1️⃣ GitHub から NYSE & NASDAQ の銘柄リストを取得
def download_txt(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ {filename} をダウンロードしました")
    else:
        print(f"❌ {filename} のダウンロードに失敗しました: {response.status_code}")

# 2️⃣ TXTファイルから Ticker リストを抽出
def extract_tickers_from_txt(nyse_file, nasdaq_file, output_file):
    nyse_df = pd.read_csv(nyse_file, header=None, names=["Ticker"])
    nasdaq_df = pd.read_csv(nasdaq_file, header=None, names=["Ticker"])
    
    all_tickers_df = pd.concat([nyse_df, nasdaq_df], ignore_index=True)
    all_tickers_df.to_csv(output_file, index=False)
    print(f"✅ {output_file} に {len(all_tickers_df)} 銘柄を保存しました")

# 3️⃣ `tickers.csv` を読み込む
def load_tickers_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df["Ticker"].tolist()

# 4️⃣ 株価データを取得
def fetch_stock_data(ticker):
    try:
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=365)
        df = yf.download(ticker, start=start_date, end=end_date)
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"❌ {ticker} のデータ取得失敗: {e}")
        return None

# 5️⃣ モメンタムを計算
def calculate_momentum(df, ticker):
    momentum = {"Ticker": ticker}
    for label, days in MOMENTUM_PERIODS.items():
        if len(df) >= days:
            momentum[label] = (df["Close"].iloc[-1] / df["Close"].iloc[-days] - 1) * 100
        else:
            momentum[label] = np.nan
    
    # Exchange 情報を追加
    momentum["Exchange"] = "NYSE" if ticker in nyse_tickers else "NASDAQ"
    return momentum

# 🚀 メイン処理
def main():
    nyse_file = "nyse_tickers.txt"
    nasdaq_file = "nasdaq_tickers.txt"
    ticker_file = "tickers.csv"

    # 🔹 NYSE & NASDAQ 銘柄リストを取得
    download_txt(NYSE_URL, nyse_file)
    download_txt(NASDAQ_URL, nasdaq_file)
    
    # 🔹 Tickerリストを作成
    extract_tickers_from_txt(nyse_file, nasdaq_file, ticker_file)
    
    # 🔹 銘柄リストを読み込み
    tickers = load_tickers_from_csv(ticker_file)
    
    global nyse_tickers
    nyse_tickers = pd.read_csv(nyse_file, header=None, names=["Ticker"])["Ticker"].tolist()
    
    results = []
    print(f"📌 {len(tickers)} 銘柄のデータ取得開始...")
    
    for i, ticker in enumerate(tickers):
        print(f"📊 {i+1}/{len(tickers)}: {ticker} のデータ取得中...")
        df = fetch_stock_data(ticker)
        
        if df is not None:
            momentum = calculate_momentum(df, ticker)
            results.append(momentum)
        
        time.sleep(1)
    
    # 📁 CSVに保存
    df_momentum = pd.DataFrame(results)
    df_momentum.to_csv("momentum_data.csv", index=False)
    print("✅ モメンタムデータ保存完了: momentum_data.csv")

if __name__ == "__main__":
    main()
