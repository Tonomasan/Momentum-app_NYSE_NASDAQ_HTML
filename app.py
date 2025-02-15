import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import matplotlib.pyplot as plt
from momentum_calculator import main
from momentum_calculator import get_stock_details

# タイトル
st.title("📈 米国株モメンタム検索アプリ")

# データ取得
st.write("⏳ データ取得中...")
df = main()
st.write("✅ データ取得完了！")

# **検索機能の追加**
st.subheader("🔍 銘柄検索")
search_query = st.text_input("ティッカーを入力 (例: AAPL, MSFT)", "").upper()

# 検索処理
if search_query:
    df = df[df["Ticker"].str.contains(search_query, na=False)]

# **データ表示**
st.subheader("📊 モメンタム一覧")
st.dataframe(df)

# **フィルタリング**
st.subheader("⚙️ フィルタリング")
min_momentum = st.slider("最低モメンタム値（%）", -100, 100, 10)
selected_period = st.selectbox("期間を選択", df.columns[1:])  # "Ticker"を除外

# フィルタリング処理
filtered_df = df[df[selected_period] >= min_momentum]
st.write(f"**{selected_period} が {min_momentum}% 以上の銘柄**")
st.dataframe(filtered_df)

# **ソート機能**
sort_order = st.radio("並び順", ["昇順", "降順"])
filtered_df = filtered_df.sort_values(by=selected_period, ascending=(sort_order == "昇順"))
st.dataframe(filtered_df)


# **グラフ表示**
st.subheader("📉 モメンタムのグラフ")



# 1つの銘柄を選択してグラフ化
selected_stock = st.selectbox("グラフを表示する銘柄を選択", df["Ticker"])
stock_data = df[df["Ticker"] == selected_stock].melt(id_vars=["Ticker"], var_name="期間", value_name="モメンタム")

fig = px.bar(stock_data, x="期間", y="モメンタム", color="モメンタム",
             color_continuous_scale="RdYlGn", title=f"{selected_stock} のモメンタム推移")

st.plotly_chart(fig, use_container_width=True, key=f"chart_{selected_stock}")
#st.plotly_chart(fig)


st.title("📈 米国株モメンタム検索アプリ")

tab1, tab2 = st.tabs(["📊 モメンタム一覧", "🔎 個別銘柄の詳細"])

with tab1:
    st.subheader("米国株モメンタム一覧")
    st.dataframe(df.style.background_gradient(cmap="RdYlGn", subset=df.columns[1:]))  # カラーマップ適用

with tab2:
    st.subheader("個別銘柄の詳細")
    selected_stock = st.selectbox("銘柄を選択", df["Ticker"])
    stock_data = df[df["Ticker"] == selected_stock].melt(id_vars=["Ticker"], var_name="期間", value_name="モメンタム")
    
    fig = px.bar(stock_data, x="期間", y="モメンタム", color="モメンタム",
                 color_continuous_scale="RdYlGn", title=f"{selected_stock} のモメンタム推移")
    st.plotly_chart(fig)


# 選択した銘柄の詳細情報を取得
details = get_stock_details(selected_stock)

st.subheader(f"📌 {details['企業名']} の詳細情報")
st.write(f"**現在価格:** {details['現在価格']}")
st.write(f"**PER:** {details['PER']} / **PBR:** {details['PBR']}")
st.write(f"**時価総額:** {details['時価総額']} / **売上:** {details['売上']}")
st.write(f"**営業利益率:** {details['営業利益']}")

# 株価チャートの表示
st.subheader("📈 過去1年の株価チャート")
chart_data = yf.Ticker(selected_stock).history(period="1y")
st.line_chart(chart_data["Close"])
