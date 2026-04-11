import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "data.db")


def normalize_columns(df):
    df.columns = [
        col.strip().replace(" ", "_").replace("-", "_").lower()
        for col in df.columns
    ]
    return df


def load_uploaded_data(file):
    df = pd.read_csv(file)
    df = normalize_columns(df)

    conn = sqlite3.connect(DB_PATH)
    table_name = "user_data"
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return table_name, df.columns.tolist(), df


def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df