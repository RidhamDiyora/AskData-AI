import sqlite3
import pandas as pd
import os
from utils.llm import fix_sql

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "data.db")


def normalize_columns(df):
    df.columns = [
        col.strip().replace(" ", "_").replace("-", "_").lower()
        for col in df.columns
    ]
    return df


def clean_column_names(df):
    df.columns = [
        col.replace("(", "_")
           .replace(")", "")
           .replace(" ", "_")
           .lower()
        for col in df.columns
    ]
    return df


# ✅ REQUIRED FUNCTION (fix import error)
def load_uploaded_data(file):
    df = pd.read_csv(file)
    df = normalize_columns(df)

    conn = sqlite3.connect(DB_PATH)
    table_name = "user_data"
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return table_name, df.columns.tolist(), df


# ✅ UPDATED RUN QUERY (with auto-fix)
def run_query(query, table_name=None, columns=None):
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql(query, conn)

    except Exception as e:
        try:
            fixed_query = fix_sql(query, str(e), table_name, columns)
            df = pd.read_sql(fixed_query, conn)
        except Exception as e2:
            conn.close()
            raise e2

    conn.close()

    df = clean_column_names(df)

    return df