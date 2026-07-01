"""
database.py
Supabaseとの通信を担当するモジュール
"""

from typing import Dict, List

import pandas as pd
import streamlit as st
from supabase import Client, create_client


# ===============================
# Supabase接続
# ===============================

@st.cache_resource
def get_supabase() -> Client:
    """
    Supabaseクライアントを取得
    """

    url = st.secrets["https://cgznchpsgdqampgcxhft.supabase.co"]
    key = st.secrets["sb_publishable_AooimLsFivuBm1w4wSoUXw_6HM2cicj"]

    return create_client(url, key)


supabase = get_supabase()


# ===============================
# 対戦登録
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
    """
    対戦データ追加
    """

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

    return (
        supabase.table("duel_records")
        .insert(data)
        .execute()
    )


# ===============================
# 全件取得
# ===============================

def get_records() -> pd.DataFrame:
    """
    全データ取得
    """

    response = (
        supabase.table("duel_records")
        .select("*")
        .order("duel_date", desc=True)
        .execute()
    )

    return pd.DataFrame(response.data)


# ===============================
# ID指定取得
# ===============================

def get_record(record_id: int):

    response = (
        supabase.table("duel_records")
        .select("*")
        .eq("id", record_id)
        .single()
        .execute()
    )

    return response.data


# ===============================
# 更新
# ===============================

def update_record(
    record_id: int,
    duel_date: str,
    deck: str,
    opponent_deck: str,
    rank: str,
    coin: str,
    turn: str,
    result: str,
    memo: str,
):

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

    return (
        supabase.table("duel_records")
        .update(data)
        .eq("id", record_id)
        .execute()
    )


# ===============================
# 削除
# ===============================

def delete_record(record_id: int):

    return (
        supabase.table("duel_records")
        .delete()
        .eq("id", record_id)
        .execute()
    )


# ===============================
# DataFrame取得
# ===============================

def get_dataframe() -> pd.DataFrame:

    df = get_records()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "id",
                "duel_date",
                "deck",
                "opponent_deck",
                "rank",
                "coin",
                "turn",
                "result",
                "memo",
                "created_at",
            ]
        )

    return df


# ===============================
# CSV用
# ===============================

def export_csv() -> bytes:

    df = get_dataframe()

    return df.to_csv(
        index=False,
        encoding="utf-8-sig"
    ).encode("utf-8-sig")


# ===============================
# 件数取得
# ===============================

def get_total_matches() -> int:

    df = get_dataframe()

    return len(df)


# ===============================
# 勝利数取得
# ===============================

def get_total_wins() -> int:

    df = get_dataframe()

    if df.empty:
        return 0

    return len(df[df["result"] == "勝ち"])


# ===============================
# 敗北数取得
# ===============================

def get_total_losses() -> int:

    df = get_dataframe()

    if df.empty:
        return 0

    return len(df[df["result"] == "負け"])
