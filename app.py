import streamlit as st
from database import add_record, get_dataframe

st.set_page_config(page_title="Master Duel Tracker", layout="wide")

st.title("🎴 Master Duel 戦績記録")


# ===============================
# 状態管理（超重要）
# ===============================

if "deck" not in st.session_state:
    st.session_state.deck = ""

if "opponent" not in st.session_state:
    st.session_state.opponent = ""

if "rank" not in st.session_state:
    st.session_state.rank = ""


# ===============================
# 入力（最低限）
# ===============================

st.subheader("📝 基本情報")

st.session_state.deck = st.text_input("自分のデッキ", st.session_state.deck)
st.session_state.opponent = st.text_input("相手デッキ", st.session_state.opponent)
st.session_state.rank = st.text_input("ランク", st.session_state.rank)


# ===============================
# ワンタップ記録ボタン
# ===============================

st.subheader("⚡ 対戦結果を記録（ワンタップ）")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏆 勝ち"):
        add_record(
            str(st.date_input("日付")),
            st.session_state.deck,
            st.session_state.opponent,
            st.session_state.rank,
            "表",          # 仮（後で選択式にできる）
            "先攻",
            "勝ち",
            ""
        )
        st.success("勝ちを記録しました")
        st.rerun()

with col2:
    if st.button("💀 負け"):
        add_record(
            str(st.date_input("日付")),
            st.session_state.deck,
            st.session_state.opponent,
            st.session_state.rank,
            "表",
            "先攻",
            "負け",
            ""
        )
        st.error("負けを記録しました")
        st.rerun()


# ===============================
# 補助ボタン（後攻など）
# ===============================

col3, col4 = st.columns(2)

with col3:
    if st.button("先攻"):
        st.session_state.turn = "先攻"

with col4:
    if st.button("後攻"):
        st.session_state.turn = "後攻"


# ===============================
# データ表示
# ===============================

st.subheader("📊 戦績")

df = get_dataframe()
st.dataframe(df)
