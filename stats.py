"""
stats.py
Master Duel Tracker - 統計計算モジュール
"""

from typing import Dict

import pandas as pd


# ===============================
# 基本フィルタ
# ===============================

def safe_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    空データ対策
    """

    if df is None or df.empty:
        return pd.DataFrame()

    return df


# ===============================
# 勝率
# ===============================

def win_rate(df: pd.DataFrame) -> float:

    df = safe_df(df)

    if len(df) == 0:
        return 0.0

    wins = df[df["result"] == "勝ち"]

    return len(wins) / len(df) * 100


# ===============================
# 先攻・後攻勝率
# ===============================

def first_second_rates(df: pd.DataFrame) -> Dict[str, float]:

    df = safe_df(df)

    if len(df) == 0:
        return {
            "first_rate": 0.0,
            "second_rate": 0.0
        }

    first = df[df["turn"] == "先攻"]
    second = df[df["turn"] == "後攻"]

    first_rate = (
        len(first[first["result"] == "勝ち"]) / len(first) * 100
        if len(first) > 0 else 0.0
    )

    second_rate = (
        len(second[second["result"] == "勝ち"]) / len(second) * 100
        if len(second) > 0 else 0.0
    )

    return {
        "first_rate": first_rate,
        "second_rate": second_rate
    }


# ===============================
# コイントス統計
# ===============================

def coin_rates(df: pd.DataFrame) -> Dict[str, float]:

    df = safe_df(df)

    if len(df) == 0:
        return {
            "head_rate": 0.0,
            "tail_rate": 0.0
        }

    head = df[df["coin"] == "表"]
    tail = df[df["coin"] == "裏"]

    total = len(df)

    return {
        "head_rate": len(head) / total * 100,
        "tail_rate": len(tail) / total * 100
    }


# ===============================
# コイントス×先攻率
# ===============================

def coin_first_analysis(df: pd.DataFrame) -> Dict[str, float]:

    df = safe_df(df)

    if len(df) == 0:
        return {
            "head_first_rate": 0.0,
            "tail_first_rate": 0.0
        }

    head = df[df["coin"] == "表"]
    tail = df[df["coin"] == "裏"]

    head_first_rate = (
        len(head[head["turn"] == "先攻"]) / len(head) * 100
        if len(head) > 0 else 0.0
    )

    tail_first_rate = (
        len(tail[tail["turn"] == "先攻"]) / len(tail) * 100
        if len(tail) > 0 else 0.0
    )

    return {
        "head_first_rate": head_first_rate,
        "tail_first_rate": tail_first_rate
    }


# ===============================
# デッキ別勝率
# ===============================

def deck_win_rates(df: pd.DataFrame) -> pd.DataFrame:

    df = safe_df(df)

    if len(df) == 0:
        return pd.DataFrame(columns=["deck", "win_rate", "matches"])

    result = (
        df.groupby("deck")
        .apply(lambda x: pd.Series({
            "win_rate": len(x[x["result"] == "勝ち"]) / len(x) * 100,
            "matches": len(x)
        }))
        .reset_index()
        .sort_values(by="win_rate", ascending=False)
    )

    return result


# ===============================
# 日別勝率
# ===============================

def daily_win_rate(df: pd.DataFrame) -> pd.DataFrame:

    df = safe_df(df)

    if len(df) == 0:
        return pd.DataFrame(columns=["duel_date", "win_rate", "matches"])

    result = (
        df.groupby("duel_date")
        .apply(lambda x: pd.Series({
            "win_rate": len(x[x["result"] == "勝ち"]) / len(x) * 100,
            "matches": len(x)
        }))
        .reset_index()
        .sort_values(by="duel_date")
    )

    return result


# ===============================
# 総合サマリー
# ===============================

def summary(df: pd.DataFrame) -> Dict:

    df = safe_df(df)

    return {
        "total_matches": len(df),
        "win_rate": win_rate(df),
        "first_second": first_second_rates(df),
        "coin": coin_rates(df),
        "coin_first": coin_first_analysis(df),
    }
