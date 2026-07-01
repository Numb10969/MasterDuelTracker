import streamlit as st
import pandas as pd
from supabase import create_client


# ===============================
# Supabase接続
# ===============================

def get_client():
    try:
        url = st.secrets["https://cgznchpsgdqampgcxhft.supabase.co"]
        key = st.secrets["sb_publishable_AooimLsFivuBm1w4wSoUXw_6HM2cicj"]
        return create_client(url, key)
    except Exception:
        return None


def client():
    return get_client()


# ===============================
# 取得（シーズン別）
# ===============================

def get_dataframe(season: str) -> pd.DataFrame:
    c = client()

    if c is None:
        return pd.DataFrame()

    try:
        res = (
            c.table("duel_records")
            .select("*")
            .eq("season", season)
            .order("duel_date", desc=True)
            .execute()
        )

        return pd.DataFrame(res.data)

    except Exception:
        return pd.DataFrame()


# ===============================
# 追加
# ===============================

def add_record(season, duel_date, deck, opponent_deck, coin, turn, result, memo):

    c = client()

    if c is None:
        return False, "Supabase未接続"

    try:
        c.table("duel_records").insert({
            "season": season,
            "duel_date": duel_date,
            "deck": deck,
            "opponent_deck": opponent_deck,
            "coin": coin,
            "turn": turn,
            "result": result,
            "memo": memo,
        }).execute()

        return True, "OK"

    except Exception as e:
        return False, str(e)
