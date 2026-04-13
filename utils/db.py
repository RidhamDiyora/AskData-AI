import sqlite3
import pandas as pd
from utils.llm import fix_sql


def run_query(query, table_name=None, columns=None):
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql(query, conn)

    except Exception as e:
        # 🔥 Try fixing SQL using LLM
        try:
            fixed_query = fix_sql(query, str(e), table_name, columns)
            df = pd.read_sql(fixed_query, conn)
        except Exception as e2:
            conn.close()
            raise e2

    conn.close()

    # Clean column names
    df.columns = [
        col.replace("(", "_")
           .replace(")", "")
           .replace(" ", "_")
           .lower()
        for col in df.columns
    ]

    return df