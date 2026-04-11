import sqlite3
import pandas as pd

DB_PATH = "db/data.db"


def normalize_columns(df):
    df.columns = [
        col.strip()
           .replace(" ", "_")
           .replace("-", "_")
           .lower()
        for col in df.columns
    ]
    return df


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df = normalize_columns(df)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ Data loaded with normalized columns")


def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        conn.close()
        raise e
    conn.close()
    return df


def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(sales);")
    columns = [col[1] for col in cursor.fetchall()]

    conn.close()
    return columns