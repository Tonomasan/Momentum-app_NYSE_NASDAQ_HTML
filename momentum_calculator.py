import pandas as pd
import numpy as np
import time
import requests
import datetime
import yfinance as yf
import os
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

    # `Symbol` カラムを取得
    nyse_nasdaq_tickers = nyse_nasdaq_df["ACT Symbol"].dropna().unique().tolist()
    #nasdaq_tickers = nasdaq_df["Symbol"].dropna().unique().tolist()

    #Stooq用
    #Stooqからデータ取得する場合 `.US` を付加
    #tickers = [ticker + ".US" for ticker in nyse_nasdaq_tickers]

    #yfinance用
    #'.US'を付加しない
    tickers = nyse_nasdaq_tickers

    # CSV に保存
    pd.DataFrame({"Ticker": tickers}).to_csv(output_file, index=False)
    print(f"✅ {output_file} に {len(tickers)} 銘柄を保存しました")

# 3️⃣ `tickers.csv` を読み込む
def load_tickers_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    tickers = df["Ticker"].tolist()
    return tickers

# 4️⃣ 株価データを取得
#Stooq用
# def fetch_stock_data(ticker):
#     try:
#         end_date = datetime.datetime.today()
#         start_date = end_date - datetime.timedelta(days=365)  # 過去1年分のデータ

#         df = pdr.get_data_stooq(ticker, start=start_date, end=end_date)
#         df = df.sort_index()  # Stooqは降順なので昇順に変更
#         return df
#     except Exception as e:
#         print(f"❌ {ticker} のデータ取得失敗: {e}")
#         return None

#yfinance用
def fetch_stock_data(ticker):
    try:
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=365)  # 過去1年分のデータ

        # 株価データ取得
        df = yf.download(ticker, start=start_date, end=end_date)

        # インデックスを datetime 型に変換（yfinance はデフォルトで datetime）
        df.index = pd.to_datetime(df.index)

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
    test_file = "other-listed_test.csv"

    ticker_file = "tickers.csv"

    # 🔹 NYSE & NASDAQ 銘柄リストを取得
    #download_csv(NYSE_CSV_URL, nyse_file)
    
    download_csv(NYSE_NASDAQ_CSV_URL, nyse_nasdaq_file)
    
    # 🔹 Tickerリストを作成
    #extract_tickers_from_csv(nyse_file, nasdaq_file, ticker_file)
    
 
    extract_tickers_from_csv(nyse_nasdaq_file, ticker_file)
    #test
    # extract_tickers_from_csv(test_file, ticker_file)
    
    # 🔹 銘柄リストを読み込み
    tickers = load_tickers_from_csv(ticker_file)
    
    results = []

    print(f"📌 {len(tickers)} 銘柄のデータ取得開始...")
    
    for i, ticker in enumerate(tickers):
        print(f"📊 {i+1}/{len(tickers)}: {ticker} のデータ取得中...")
        df = fetch_stock_data(ticker)
        
        if df is not None:
            #test
            # filename = f"tickers_data_yf_{i}.csv"  # i を末尾に追加
            # df.to_csv(filename, index=False)  # i を追加したファイル名で保存
            momentum = calculate_momentum(df)
            results.append({"Ticker": ticker, **momentum})

        time.sleep(1)  # 🔹 API制限を避けるために1秒待機
    
    # 現在のスクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 保存するCSVファイルのパスを作成
    csv_path = os.path.join(script_dir, "momentum_data.csv")
    # 📁 CSVに保存
    df_momentum = pd.DataFrame(results)
    #df_momentum.to_csv("momentum_data.csv", index=False)
    df_momentum.to_csv(csv_path, index=False)

    #app.pyでyfinanceを使う場合Ticker末尾".US"を削除する
    # CSVファイルを読み込む
    df = pd.read_csv('momentum_data.csv')
    # Ticker列の末尾に '.US' が含まれている行の '.US' を除去
    df['Ticker'] = df['Ticker'].str.replace(r'\.US$', '', regex=True)
    # 新しいCSVとして保存
    csv_path_yf = os.path.join(script_dir, "momentum_data_yf.csv")
    # df.to_csv('momentum_data_yf.csv', index=False)
    df.to_csv(csv_path, index=False)

    print("✅ モメンタムデータ保存完了: momentum_data.csv, momentum_data_yf.csv")

if __name__ == "__main__":
    main()
