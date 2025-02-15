import pandas as pd
import numpy as np
import time
import requests
from pandas_datareader import data as pdr

# 📌 NYSE & NASDAQ 銘柄リストの GitHub URL
#NYSE_CSV_URL = "https://raw.githubusercontent.com/datasets/nyse-other-listings/main/data/nyse-listed.csv"
NYSE_NASDAQ_CSV_URL = "https://raw.githubusercontent.com/datasets/nyse-other-listings/main/data/other-listed.csv"

# ⏳ 過去何日間のモメンタムを計算するか設定
MOMENTUM_PERIODS = {
    "1w": 5,    # 1週間
    "1m": 21,   # 1か月
    "3m": 63,   # 3か月
    "6m": 126,  # 6か月
    "1y": 252   # 1年
}

# 1️⃣ GitHub から NYSE & NASDAQ の銘柄リストを取得
def download_csv(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ {filename} をダウンロードしました")
    else:
        print(f"❌ {filename} のダウンロードに失敗しました: {response.status_code}")

# 2️⃣ CSVから Ticker リストを抽出
def extract_tickers_from_csv(nyse_nasdaq_file, output_file):
    nyse_nasdaq_df = pd.read_csv(nyse_nasdaq_file)
    #nasdaq_df = pd.read_csv(nasdaq_file)

    # `Symbol` カラムを取得し、Stooq 用に `.US` を付加
    nyse_nasdaq_tickers = nyse_nasdaq_df["ACT Symbol"].dropna().unique().tolist()
    #nasdaq_tickers = nasdaq_df["Symbol"].dropna().unique().tolist()

    tickers = [ticker + ".US" for ticker in nyse_nasdaq_tickers]

    # CSV に保存
    pd.DataFrame({"Ticker": tickers}).to_csv(output_file, index=False)
    print(f"✅ {output_file} に {len(tickers)} 銘柄を保存しました")

# 3️⃣ `tickers.csv` を読み込む
def load_tickers_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    tickers = df["Ticker"].tolist()
    return tickers

# 4️⃣ 株価データを取得
def fetch_stock_data(ticker):
    try:
        df = pdr.get_data_stooq(ticker)
        df = df.sort_index()  # Stooqは降順なので昇順に変更
        return df
    except Exception as e:
        print(f"❌ {ticker} のデータ取得失敗: {e}")
        return None

# 5️⃣ モメンタムを計算
def calculate_momentum(df):
    momentum = {}
    for label, days in MOMENTUM_PERIODS.items():
        if len(df) >= days:
            momentum[label] = (df["Close"].iloc[-1] / df["Close"].iloc[-days] - 1) * 100
        else:
            momentum[label] = np.nan
    return momentum

# 🚀 メイン処理
def main():
    # nyse_file = "nyse-listed.csv"
    # nasdaq_file = "other-listed.csv"
    nyse_nasdaq_file = "other-listed.csv"
    ticker_file = "tickers.csv"

    # 🔹 NYSE & NASDAQ 銘柄リストを取得
    #download_csv(NYSE_CSV_URL, nyse_file)
    
    #test
    # download_csv(NYSE_NASDAQ_CSV_URL, nyse_nasdaq_file)
    
    # 🔹 Tickerリストを作成
    #extract_tickers_from_csv(nyse_file, nasdaq_file, ticker_file)
    extract_tickers_from_csv(nyse_nasdaq_file, ticker_file)
    
    # 🔹 銘柄リストを読み込み
    tickers = load_tickers_from_csv(ticker_file)
    
    results = []

    print(f"📌 {len(tickers)} 銘柄のデータ取得開始...")
    
    for i, ticker in enumerate(tickers):
        print(f"📊 {i+1}/{len(tickers)}: {ticker} のデータ取得中...")
        df = fetch_stock_data(ticker)
        
        if df is not None:
            momentum = calculate_momentum(df)
            results.append({"Ticker": ticker, **momentum})

        time.sleep(0.1)  # 🔹 API制限を避けるために1秒待機
    
    # 📁 CSVに保存
    df_momentum = pd.DataFrame(results)
    df_momentum.to_csv("momentum_data.csv", index=False)
    print("✅ モメンタムデータ保存完了: momentum_data.csv")

if __name__ == "__main__":
    main()
