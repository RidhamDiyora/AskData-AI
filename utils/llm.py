import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def clean_sql(response, table_name, columns):
    response = response.replace("```sql", "").replace("```", "").strip()

    match = re.search(r"(SELECT .*?;)", response, re.IGNORECASE | re.DOTALL)
    sql = match.group(1).strip() if match else response.strip()

    # ✅ Fix EXTRACT → SQLite
    sql = re.sub(
        r"EXTRACT\s*\(\s*YEAR\s+FROM\s+(\w+)\)",
        r"strftime('%Y', \1)",
        sql,
        flags=re.IGNORECASE
    )

    # ✅ Normalize column names (CRITICAL FIX)
    for col in columns:
        sql = re.sub(rf"\b{col}\b", col, sql, flags=re.IGNORECASE)

    # ✅ Force correct table name
    sql = re.sub(r"\bFROM\s+\w+", f"FROM {table_name}", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\bJOIN\s+\w+", f"JOIN {table_name}", sql, flags=re.IGNORECASE)

    return sql


def rewrite_question(question, history):
    context = "\n".join([m["content"] for m in history[-3:]])

    prompt = f"""
Rewrite the user question into a clear standalone question.

Conversation:
{context}

User question:
{question}

Return only the rewritten question.
"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )

    return response.json()['response'].strip()


def generate_sql(question, table_name, columns):
    prompt = f"""
You are an expert data analyst using SQLite.

Convert the question into SQL.

STRICT RULES:
- Output ONLY SQL
- Use ONLY table: {table_name}
- Use ONLY columns: {', '.join(columns)}
- Column names are case-sensitive
- Use EXACT column names
- SQL must start with SELECT and end with ;

SQL RULES:
- Use strftime('%Y', column_name) for year
- DO NOT use EXTRACT()

Question:
{question}

SQL:
"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )

    return clean_sql(response.json()['response'], table_name, columns)


def fix_sql(bad_sql, error, table_name, columns):
    prompt = f"""
Fix this SQL for SQLite:

{bad_sql}

Error:
{error}

STRICT RULES:
- Use SQLite syntax only
- Use EXACT column names
- Return ONLY SQL

Table: {table_name}
Columns: {', '.join(columns)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )

    return clean_sql(response.json()['response'], table_name, columns)


def generate_insight(df):
    prompt = f"""
Analyze the data and give 2 concise business insights:

{df.head(20).to_string()}
"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )

    return response.json()['response']