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

# モメンタムの `NaN` は 0 で埋める
df.fillna(0, inplace=True)

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
momentum_min_1w, momentum_max_1w = st.sidebar.slider("1週間モメンタム", -50, 100, (-10, 30))
momentum_min_1m, momentum_max_1m = st.sidebar.slider("1ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_3m, momentum_max_3m = st.sidebar.slider("3ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_6m, momentum_max_6m = st.sidebar.slider("6ヶ月モメンタム", -50, 100, (-10, 30))
momentum_min_1y, momentum_max_1y = st.sidebar.slider("1年モメンタム", -50, 100, (-10, 30))


# フィルタ処理（スライダー値を利用）
filtered_df = df[
    (df["1w"] >= momentum_min_1w) & (df["1w"] <= momentum_max_1w) &
    (df["1m"] >= momentum_min_1m) & (df["1m"] <= momentum_max_1m) &
    (df["3m"] >= momentum_min_3m) & (df["3m"] <= momentum_max_3m) &
    (df["6m"] >= momentum_min_6m) & (df["6m"] <= momentum_max_6m) &
    (df["1y"] >= momentum_min_1y) & (df["1y"] <= momentum_max_1y)
]

# フィルタ後のデータを表示
st.write("🔢 フィルタ後のデータ件数:", len(filtered_df))
#st.write("📌 フィルタ後のデータ:", filtered_df)
#st.write(filtered_df)

# セッション状態の初期化
if "selected_ticker" not in st.session_state:
    st.session_state["selected_ticker"] = None

# DataFrameを表示（選択可能にする）
selected_rows = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    key="data_editor"
)

# 選択された行の処理
if selected_rows:
    selected_ticker = df.iloc[selected_rows[0]]["Ticker"]
    st.session_state["selected_ticker"] = selected_ticker

    # モーダル（ポップアップ）を開く
    with st.modal(f"📊 {selected_ticker} のチャート"):
        tradingview_url = f"https://jp.tradingview.com/chart/?symbol=NASDAQ%3A{selected_ticker}"
        st.markdown(f'<iframe src="{tradingview_url}" width="700" height="500"></iframe>', unsafe_allow_html=True)




if filtered_df.empty:
    st.warning("⚠ フィルタ結果が空です。条件を緩めてください。")

search_query = st.text_input("🔍 Ticker を入力してください", "")
if search_query:
    filtered_df = filtered_df[
        filtered_df["Ticker"].str.contains(search_query, case=False, na=False)

    ]

# テーブル表示
# st.dataframe(filtered_df)


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

        # # データの列を確認（デバッグ用）
        # st.write(stock_data.columns)

        # 'Close' 列を使用して株価推移を描画
        if 'Close' in stock_data.columns:
            fig = px.line(stock_data, x=stock_data.index, y="Close", title=f"{selected_ticker} の株価推移")
            st.plotly_chart(fig)
        else:
            st.error("❌ 株価データの取得に失敗しました: 'Close' 列が見つかりませんでした")

    except Exception as e:
        st.error(f"❌ 株価データの取得に失敗しました: {e}")

# 🔹 **フィルタ後のデータもダウンロード可能に**
filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 フィルタ後のデータをダウンロード",
    data=filtered_csv,
    file_name="filtered_momentum_data.csv",
    mime="text/csv"
)
