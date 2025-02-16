import streamlit as st
import pandas as pd
import plotly.express as px
import pandas_datareader.data as web
import datetime
import io
import yfinance as yf

#app.pyの前にmomentum_calculator.pyを実行、momentum_data.csvを出力する

# CSV データを読み込み
# Stooq用
# df = pd.read_csv("momentum_data.csv")
# yfinance用
df = pd.read_csv("momentum_data_yf.csv")

# 🔹 Ticker のデータクリーニング
df = df.dropna(subset=["Ticker"])  # NaNを削除
df["Ticker"] = df["Ticker"].astype(str).str.strip()  # 文字列に変換 + 空白削除

# デバッグ用: データ確認
st.write("📌 `Ticker` のユニークな値:", df["Ticker"].unique())
st.write("📌 `Ticker` のデータ型:", df["Ticker"].dtype)
#test
st.write(df.dtypes)
st.write("📌 `df` の最初の数行:", df.head())  # データの中身を確認
st.write("📌 `df` のデータ型:", df.dtypes)  # 各カラムのデータ型を確認

# UIタイトル
st.title("📈 米国株モメンタム検索アプリ")

# 🔹 **モメンタムデータのダウンロードボタン**
st.sidebar.header("📂 データエクスポート")
csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="📥 モメンタムデータをダウンロード",
    data=csv,
    #file_name="momentum_data.csv",
    file_name="momentum_data_yf.csv",
    mime="text/csv"
)

# モメンタム期間別スライダー
st.sidebar.header("📊 モメンタム期間別フィルタ")
# momentum_min_1w, momentum_max_1w = st.sidebar.slider("1週間モメンタム", -50, 100, (-10, 30))
momentum_min_1w, momentum_max_1w = st.sidebar.slider("1週間モメンタム", -100, 100, (-100, 100))
momentum_min_1m, momentum_max_1m = st.sidebar.slider("1ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_3m, momentum_max_3m = st.sidebar.slider("3ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_6m, momentum_max_6m = st.sidebar.slider("6ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_1y, momentum_max_1y = st.sidebar.slider("1年モメンタム", -50, 100, (-10, 30))

# 並び順
sort_order = st.radio("並び順", ["昇順 (低い順)", "降順 (高い順)"])

#test
st.write(df.columns)

#test
# # モメンタム条件に基づいてフィルタリング
# filtered_df = df[
#     (df["1w"] >= momentum_min_1w) & (df["1w"] <= momentum_max_1w) &
#     (df["1m"] >= momentum_min_1m) & (df["1m"] <= momentum_max_1m) &
#     (df["3m"] >= momentum_min_3m) & (df["3m"] <= momentum_max_3m) &
#     (df["6m"] >= momentum_min_6m) & (df["6m"] <= momentum_max_6m) &
#     (df["1y"] >= momentum_min_1y) & (df["1y"] <= momentum_max_1y)
# ]

#test
# 🔹 フィルタを適用せずに全データを表示（テスト用）
filtered_df = df

# デバッグ用
st.write("📌 フィルタ適用前のデータ:", filtered_df)
st.write("🔢 フィルタ適用前のデータ件数:", len(filtered_df))

#test
st.write("📌 フィルタ後のデータ:", filtered_df)
st.write("🔢 フィルタ後のデータ件数:", len(filtered_df))
st.write("📌 フィルタ後の Ticker リスト:", filtered_df["Ticker"].unique())
st.write("📌 Ticker 列のデータ型:", filtered_df["Ticker"].dtype)

st.write("📌 読み込んだデータ（最初の5行）:", df.head())
st.write("📌 データ件数:", len(df))
st.write("📌 データのカラム:", df.columns)

if filtered_df.empty:
    st.warning("⚠ フィルタ結果が空です。条件を緩めてください。")

#test
if "Ticker" not in df.columns:
    st.error("❌ 'Ticker' 列が見つかりません！CSV のヘッダーを確認してください。")
st.write("📌 `Ticker` カラムのデータ型:", df["Ticker"].dtype)
df["Ticker"] = df["Ticker"].astype(str)  # 文字列に変換

#test
st.write("📌 `Ticker` の欠損値（NaN）の数:", df["Ticker"].isna().sum())
st.write("📌 `Ticker` のユニーク値:", df["Ticker"].unique())
df = df.dropna(subset=["Ticker"])  # NaNを含む行を削除
df["Ticker"] = df["Ticker"].astype(str)  # 念のため再変換


# 検索キーワードで絞り込み
# search_query = st.text_input("🔍 Ticker または企業名を入力してください", "")
# if search_query:
#     filtered_df = filtered_df[
#         filtered_df["Ticker"].str.contains(search_query, case=False, na=False) |
#         filtered_df["Company"].str.contains(search_query, case=False, na=False)
#     ]
search_query = st.text_input("🔍 Ticker を入力してください", "")
if search_query:
    filtered_df = filtered_df[
        filtered_df["Ticker"].str.contains(search_query, case=False, na=False)

    ]


# 並び替え（昇順・降順）
ascending = True if sort_order == "昇順 (低い順)" else False
filtered_df = filtered_df.sort_values(by="1y", ascending=ascending)

# テーブル表示
st.dataframe(filtered_df)

# 🔹 **フィルタ後のデータもダウンロード可能に**
filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 フィルタ後のデータをダウンロード",
    data=filtered_csv,
    file_name="filtered_momentum_data.csv",
    mime="text/csv"
)

# 選択した銘柄の詳細を表示
selected_ticker = st.selectbox("📌 詳細を表示する銘柄を選択", filtered_df["Ticker"].unique())

#Stooqからデータ取得
# if selected_ticker:
#     st.subheader(f"📉 {selected_ticker} の株価チャート")

#     # 過去1年間の株価データを取得
#     start_date = datetime.datetime.now() - datetime.timedelta(days=365)
#     end_date = datetime.datetime.now()

#     try:
#         stock_data = web.DataReader(selected_ticker, "stooq", start_date, end_date)

#         # Stooqのデータは日付が降順なので、昇順に並び替え
#         stock_data = stock_data.sort_index()

#         # チャートを描画
#         fig = px.line(stock_data, x=stock_data.index, y="Close", title=f"{selected_ticker} の株価推移")
#         st.plotly_chart(fig)

#     except Exception as e:
#         st.error(f"❌ 株価データの取得に失敗しました: {e}")

#yfinanceからデータ取得
if selected_ticker:
    st.subheader(f"📉 {selected_ticker} の株価チャート")

    # 過去1年間の株価データを取得
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.datetime.now()

    try:
        # yfinanceを使用して株価データを取得
        stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

        # データの列を確認（デバッグ用）
        st.write(stock_data.columns)

        # 'Close' 列を使用して株価推移を描画
        if 'Close' in stock_data.columns:
            fig = px.line(stock_data, x=stock_data.index, y="Close", title=f"{selected_ticker} の株価推移")
            st.plotly_chart(fig)
        else:
            st.error("❌ 株価データの取得に失敗しました: 'Close' 列が見つかりませんでした")

    except Exception as e:
        st.error(f"❌ 株価データの取得に失敗しました: {e}")