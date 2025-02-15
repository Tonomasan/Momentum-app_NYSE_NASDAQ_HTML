import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import matplotlib.pyplot as plt

# 📌 アプリタイトル
st.title("📈 米国株モメンタム検索アプリ")

# 📌 ダミーデータ（本番はDBやAPIから取得）
df = pd.DataFrame({
    "Ticker": ["AAPL", "MSFT", "GOOGL"],
    "1M (%)": [10, -5, 15],
    "3M (%)": [25, 8, 20],
    "6M (%)": [40, 18, 30],
})

# 📌 銘柄検索（フィルタリング）
search_query = st.text_input("🔍 銘柄を検索（例: AAPL）", "")
filtered_df = df[df["Ticker"].str.contains(search_query.upper(), na=False)] if search_query else df

# 📌 UI（タブ形式）
tab1, tab2 = st.tabs(["📊 モメンタム一覧", "🔎 個別銘柄の詳細"])

with tab1:
    st.subheader("📊 モメンタム一覧")
    st.dataframe(filtered_df.style.background_gradient(cmap="RdYlGn", subset=df.columns[1:]))

with tab2:
    selected_stock = st.selectbox("銘柄を選択", df["Ticker"])
    
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

    details = get_stock_details(selected_stock)

    # 📌 銘柄詳細データ表示
    st.subheader(f"📌 {details['企業名']} の詳細情報")
    st.write(f"**現在価格:** {details['現在価格']}")
    st.write(f"**PER:** {details['PER']} / **PBR:** {details['PBR']}")
    st.write(f"**時価総額:** {details['時価総額']} / **売上:** {details['売上']}")
    st.write(f"**営業利益率:** {details['営業利益']}")

    # 📌 株価チャート
    st.subheader("📈 過去1年の株価チャート")
    chart_data = yf.Ticker(selected_stock).history(period="1y")
    st.line_chart(chart_data["Close"])
