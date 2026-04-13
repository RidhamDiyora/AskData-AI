import re
import os
from groq import Groq

# 🔥 Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ✅ Clean SQL (fix columns + enforce table)
def clean_sql(response, table_name, columns):
    response = response.strip()

    match = re.search(r"(SELECT .*?;)", response, re.IGNORECASE | re.DOTALL)
    sql = match.group(1).strip() if match else response.strip()

    # Normalize column names (case fix)
    for col in columns:
        sql = re.sub(rf"\b{col}\b", col, sql, flags=re.IGNORECASE)

    # Force correct table name
    sql = re.sub(r"\bFROM\s+\w+", f"FROM {table_name}", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\bJOIN\s+\w+", f"JOIN {table_name}", sql, flags=re.IGNORECASE)

    return sql


# 🔥 Generic LLM call
def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # fast + powerful
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# 🧠 Rewrite vague questions (context-aware)
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

STRICT RULES:
- Output ONLY SQL
- Use ONLY table: {table_name}
- Use ONLY columns: {', '.join(columns)}
- Column names are lowercase
- SQL must start with SELECT and end with ;

SQL RULES:
- Use strftime('%Y', column_name) for year
- DO NOT use EXTRACT()

Question:
{question}
"""

    response = ask_llm(prompt)
    return clean_sql(response, table_name, columns)


# 🔧 Fix broken SQL
def fix_sql(bad_sql, error, table_name, columns):
    prompt = f"""
Fix this SQL query for SQLite:

{bad_sql}

Error:
{error}

STRICT RULES:
- Use correct column names
- Use SQLite syntax
- Return ONLY SQL

Table: {table_name}
Columns: {', '.join(columns)}
"""

    response = ask_llm(prompt)
    return clean_sql(response, table_name, columns)


# 📊 Generate insights
def generate_insight(df):
    prompt = f"""
Analyze this data and give 2 short business insights:

{df.head(20).to_string()}
"""

    return ask_llm(prompt)