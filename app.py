"""
Master Duel Tracker
Streamlit メインUI
"""

import streamlit as st
import pandas as pd

from database import (
    add_record,
    get_dataframe,
    delete_record,
)

import stats as stats


# ===============================
# ページ設定
# ===============================

st.set_page_config(
    page_title="Master Duel Tracker",
    layout="wide"
)

st.title("🎴 Master Duel 戦績管理ツール")


# ===============================
# データ取得
# ===============================

df = get_dataframe()


# ===============================
# サイドバー（入力フォーム）
# ===============================

st.sidebar.header("➕ 対戦記録を追加")

with st.sidebar.form("add_form"):

    duel_date = st.date_input("日付")

    deck = st.text_input("自分のデッキ")

    opponent_deck = st.text_input("相手デッキ（任意）")

    rank = st.text_input("ランク（任意）")

    coin = st.radio("コイントス", ["表", "裏"])

    turn = st.radio("先攻 / 後攻", ["先攻", "後攻"])

    result = st.radio("勝敗", ["勝ち", "負け"])

    memo = st.text_area("メモ（任意）")

    submitted = st.form_submit_button("登録")

    if submitted:

        add_record(
            str(duel_date),
            deck,
            opponent_deck,
            rank,
            coin,
            turn,
            result,
            memo
        )

        st.success("登録しました")
        st.rerun()


# ===============================
# 統計処理
# ===============================

summary = stats.summary(df)
first_second = summary["first_second"]
coin = summary["coin"]
coin_first = summary["coin_first"]


# ===============================
# KPI表示
# ===============================

st.subheader("📊 全体統計")

col1, col2, col3, col4 = st.columns(4)

col1.metric("総試合数", summary["total_matches"])
col2.metric("勝率", f"{summary['win_rate']:.1f}%")
col3.metric("先攻勝率", f"{first_second['first_rate']:.1f}%")
col4.metric("後攻勝率", f"{first_second['second_rate']:.1f}%")


st.divider()


# ===============================
# コイントス統計
# ===============================

st.subheader("🪙 コイントス傾向")

col1, col2 = st.columns(2)

col1.metric("表率", f"{coin['head_rate']:.1f}%")
col2.metric("裏率", f"{coin['tail_rate']:.1f}%")


st.subheader("🧠 コイントス × 先攻率")

col1, col2 = st.columns(2)

col1.metric("表→先攻率", f"{coin_first['head_first_rate']:.1f}%")
col2.metric("裏→先攻率", f"{coin_first['tail_first_rate']:.1f}%")


st.divider()


# ===============================
# デッキ別勝率
# ===============================

st.subheader("🏆 デッキ別勝率")

deck_stats = stats.deck_win_rates(df)

if not deck_stats.empty:
    st.dataframe(deck_stats, use_container_width=True)
else:
    st.info("データがありません")


st.divider()


# ===============================
# 日別勝率
# ===============================

st.subheader("📅 日別勝率")

daily = stats.daily_win_rate(df)

if not daily.empty:
    st.line_chart(daily.set_index("duel_date")["win_rate"])
    st.dataframe(daily, use_container_width=True)
else:
    st.info("データがありません")


st.divider()


# ===============================
# 戦績一覧
# ===============================

st.subheader("📋 戦績一覧")

if not df.empty:

    st.dataframe(
        df.sort_values("duel_date", ascending=False),
        use_container_width=True
    )

    # ===========================
    # 削除機能
    # ===========================

    st.subheader("🗑️ 削除")

    delete_id = st.number_input("削除するID", min_value=0, step=1)

    if st.button("削除実行"):

        delete_record(int(delete_id))
        st.success("削除しました")
        st.rerun()

else:
    st.info("まだデータがありません")
