import streamlit as st
from database import add_record, get_dataframe


# ===============================
# 初期設定
# ===============================

st.set_page_config(page_title="Master Duel Tracker", layout="wide")

st.title("🎴 Master Duel 戦績管理")


# ===============================
# シーズン管理
# ===============================

if "season" not in st.session_state:
    st.session_state.season = "2026-S1"

st.sidebar.header("📅 シーズン管理")

st.sidebar.write(f"現在: {st.session_state.season}")

if st.sidebar.button("➕ 新シーズン"):
    num = int(st.session_state.season[-1]) + 1
    st.session_state.season = f"2026-S{num}"
    st.rerun()


# ===============================
# 入力UI
# ===============================

st.subheader("🎮 試合入力")

deck = st.text_input("自分のデッキ")
opponent = st.text_input("相手デッキ")

col1, col2 = st.columns(2)

with col1:
    result = st.radio("勝敗", ["勝ち", "負け"])

with col2:
    coin = st.radio("コイントス", ["表", "裏"])

turn = st.radio("先攻 / 後攻", ["先攻", "後攻"])

date = st.date_input("日付")


# ===============================
# 保存
# ===============================

if st.button("📥 記録する"):

    ok, msg = add_record(
        st.session_state.season,
        str(date),
        deck,
        opponent,
        coin,
        turn,
        result,
        ""
    )

    if ok:
        st.success("記録しました")
        st.rerun()
    else:
        st.error(msg)


# ===============================
# データ取得
# ===============================

df = get_dataframe(st.session_state.season)


# ===============================
# 統計
# ===============================

st.subheader("📊 統計")

if not df.empty:

    total = len(df)
    win = len(df[df["result"] == "勝ち"])

    first = len(df[df["turn"] == "先攻"])
    coin_head = len(df[df["coin"] == "表"])

    col1, col2, col3 = st.columns(3)

    col1.metric("勝率", f"{win/total*100:.1f}%")
    col2.metric("先攻率", f"{first/total*100:.1f}%")
    col3.metric("表率", f"{coin_head/total*100:.1f}%")

else:
    st.info("データなし")


# ===============================
# 一覧
# ===============================

st.subheader("📋 戦績一覧")

st.dataframe(df)
