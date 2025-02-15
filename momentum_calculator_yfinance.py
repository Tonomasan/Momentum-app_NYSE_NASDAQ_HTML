import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 銘柄リスト（必要に応じて追加）
TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META"]

# 取得する期間
PERIOD = "1y"  # 1年前からのデータ

# モメンタム計算用の期間（営業日ベース）
MOMENTUM_PERIODS = {
    "1ヶ月": 21,    # 約21営業日
    "3ヶ月": 63,    # 約63営業日
    "6ヶ月": 126,   # 約126営業日
    "12ヶ月": 252   # 約252営業日
}

def get_stock_data(ticker):
    """指定した銘柄の過去1年分の株価データを取得"""
    stock = yf.Ticker(ticker)
    df = stock.history(period=PERIOD)
    return df["Close"]  # 終値のみ取得

def calculate_momentum(close_prices):
    """終値データをもとにモメンタムを計算"""
    momentum_data = {}
    for period_name, days in MOMENTUM_PERIODS.items():
        if len(close_prices) > days:
            momentum = (close_prices[-1] - close_prices[-days]) / close_prices[-days] * 100
            momentum_data[period_name] = round(momentum, 2)
        else:
            momentum_data[period_name] = None  # データ不足時
    return momentum_data

def main():
    results = []
    for ticker in TICKERS:
        try:
            close_prices = get_stock_data(ticker)
            momentum = calculate_momentum(close_prices)
            momentum["Ticker"] = ticker
            results.append(momentum)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # 結果をデータフレーム化
    df = pd.DataFrame(results)
    df = df[["Ticker"] + list(MOMENTUM_PERIODS.keys())]  # 列順を整理
    return df


def get_stock_details(ticker):
    """指定した銘柄の詳細情報を取得"""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "企業名": info.get("longName", "N/A"),
        "現在価格": info.get("currentPrice", "N/A"),
        "PER": info.get("trailingPE", "N/A"),
        "PBR": info.get("priceToBook", "N/A"),
        "時価総額": info.get("marketCap", "N/A"),
        "売上": info.get("totalRevenue", "N/A"),
        "営業利益": info.get("operatingMargins", "N/A"),
    }


if __name__ == "__main__":
    df = main()
    print(df)  # デバッグ用


