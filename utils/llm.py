import re
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 LLM call with fallback (future-proof)
def ask_llm(prompt):
    models = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = str(e)
            continue

    return f"⚠️ LLM Error: {last_error}"


# ✅ Clean SQL output
def clean_sql(response, table_name, columns):
    response = response.strip()

    match = re.search(r"(SELECT .*?;)", response, re.IGNORECASE | re.DOTALL)
    sql = match.group(1).strip() if match else response.strip()

    # Normalize column names
    for col in columns:
        sql = re.sub(rf"\b{col}\b", col, sql, flags=re.IGNORECASE)

    # Force correct table
    sql = re.sub(r"\bFROM\s+\w+", f"FROM {table_name}", sql, flags=re.IGNORECASE)

    return sql


# 🧠 Rewrite question
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

    return ask_llm(prompt)


# 🧠 Generate SQL
def generate_sql(question, table_name, columns):
    prompt = f"""
You are an expert data analyst using SQLite.

Convert the question into SQL.

RULES:
- Only return SQL
- Use table: {table_name}
- Use columns: {', '.join(columns)}
- Avoid SELECT *
- Use aggregation for large data
- Always use aliases (AS name)
- Use SQLite syntax only
- Use strftime('%Y', column) for year
- Output must end with ;

Question:
{question}
"""

    response = ask_llm(prompt)
    return clean_sql(response, table_name, columns)


# 🔧 Fix SQL errors
def fix_sql(bad_sql, error, table_name, columns):
    prompt = f"""
Fix this SQL query for SQLite:

{bad_sql}

Error:
{error}

RULES:
- Return ONLY SQL
- Use correct column names
- Use SQLite syntax
- Keep same intent

Table: {table_name}
Columns: {', '.join(columns)}
"""

    response = ask_llm(prompt)
    return clean_sql(response, table_name, columns)


# 📊 🔥 FINAL INSIGHT SYSTEM (SMART + ACCURATE)
def generate_insight(df):
    if df is None or df.empty:
        return "No data available for insights."

    # 🔥 Detect aggregated results
    if len(df) <= 10 and df.shape[1] <= 3:
        prompt = f"""
You are a data analyst.

This is aggregated data (already summarized).

Give 2-3 clear and correct insights.

RULES:
- Use exact numbers from data
- DO NOT assume total rows = dataset size
- Compare values if possible
- Keep it short and factual

DATA:
{df.to_string()}
"""
    else:
        # 🔥 Use structured summary for large/raw data
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        summary = ""

        if numeric_cols:
            summary += "\nNUMERIC SUMMARY:\n"
            summary += df[numeric_cols].describe().to_string()

        if categorical_cols:
            summary += "\n\nCATEGORICAL SAMPLE:\n"
            for col in categorical_cols[:3]:
                summary += f"\n{col}: {df[col].value_counts().head(5).to_string()}\n"

        prompt = f"""
You are a data analyst.

Based ONLY on the summary below, give 2-3 insights.

RULES:
- Be factual
- Use numbers
- No assumptions
- Keep it short

DATA SUMMARY:
{summary}
"""

    return ask_llm(prompt)