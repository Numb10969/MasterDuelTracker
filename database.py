"""
database.py
Supabaseとの通信を担当するモジュール（完全版）
"""

import pandas as pd
import streamlit as st
from typing import Optional
from supabase import create_client, Client


# ===============================
# Supabase接続
# ===============================

@st.cache_resource
def get_supabase() -> Optional[Client]:
    """
    Supabaseクライアント取得（安全版）
    - secrets未設定でもクラッシュしない
    """

    try:
        # ★ここが正しい書き方（超重要）
        url = st.secrets["https://cgznchpsgdqampgcxhft.supabase.co"]
        key = st.secrets["sb_publishable_AooimLsFivuBm1w4wSoUXw_6HM2cicj"]

        if not url or not key:
            return None

        return create_client(url, key)

    except Exception as e:
        st.error(f"Supabase接続エラー: {e}")
        return None


supabase = get_supabase()


# ===============================
# 接続チェック
# ===============================

def is_connected() -> bool:
    return supabase is not None


# ===============================
# データ取得
# ===============================

def get_dataframe() -> pd.DataFrame:

    if supabase is None:
        return pd.DataFrame()

    try:
        res = (
            supabase.table("duel_records")
            .select("*")
            .order("duel_date", desc=True)
            .execute()
        )

        return pd.DataFrame(res.data)

    except Exception as e:
        st.error(f"データ取得エラー: {e}")
        return pd.DataFrame()


# ===============================
# データ追加
# ===============================

def add_record(
    duel_date: str,
    deck: str,
    opponent_deck: str,
    rank: str,
    coin: str,
    turn: str,
    result: str,
    memo: str,
):

    if supabase is None:
        st.error("Supabase未接続（Secretsを確認してください）")
        return None

    try:
        data = {
            "duel_date": duel_date,
            "deck": deck,
            "opponent_deck": opponent_deck,
            "rank": rank,
            "coin": coin,
            "turn": turn,
            "result": result,
            "memo": memo,
        }

        return supabase.table("duel_records").insert(data).execute()

    except Exception as e:
        st.error(f"登録エラー: {e}")
        return None


# ===============================
# データ削除
# ===============================

def delete_record(record_id: int):

    if supabase is None:
        st.error("Supabase未接続")
        return None

    try:
        return (
            supabase.table("duel_records")
            .delete()
            .eq("id", record_id)
            .execute()
        )

    except Exception as e:
        st.error(f"削除エラー: {e}")
        return None


# ===============================
# 件数系
# ===============================

def get_total_matches() -> int:
    df = get_dataframe()
    return len(df)


def get_total_wins() -> int:
    df = get_dataframe()
    if df.empty:
        return 0
    return len(df[df["result"] == "勝ち"])


def get_total_losses() -> int:
    df = get_dataframe()
    if df.empty:
        return 0
    return len(df[df["result"] == "負け"])


# ===============================
# CSV出力
# ===============================

def export_csv() -> bytes:

    df = get_dataframe()

    return df.to_csv(
        index=False,
        encoding="utf-8-sig"
    ).encode("utf-8-sig")
