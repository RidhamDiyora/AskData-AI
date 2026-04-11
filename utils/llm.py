import requests
import re
from utils.db import get_schema

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def clean_sql(response):
    response = response.replace("```sql", "").replace("```", "").strip()

    # Extract SQL only
    match = re.search(r"(SELECT .*?;)", response, re.IGNORECASE | re.DOTALL)

    if match:
        sql = match.group(1).strip()
    else:
        sql = response.strip()

    # ✅ Fix column names
    sql = sql.replace("Order_Date", "order_date")
    sql = sql.replace("Order Date", "order_date")
    sql = sql.replace("Sales", "sales")
    sql = sql.replace("Profit", "profit")
    sql = sql.replace("Category", "category")
    sql = sql.replace("Region", "region")

    # ✅ Force correct table name
    sql = re.sub(r"\bFROM\s+\w+", "FROM sales", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\bJOIN\s+\w+", "JOIN sales", sql, flags=re.IGNORECASE)

    return sql


def generate_sql(question):
    columns = get_schema()

    prompt = f"""
You are an expert data analyst.

Convert the question into a valid SQLite SQL query.

STRICT RULES:
- Output ONLY SQL
- DO NOT explain anything
- SQL must start with SELECT
- SQL must end with ;
- ONLY use table name: sales
- DO NOT use any other table name
- Use lowercase column names

Table: sales
Columns: {', '.join(columns)}

IMPORTANT:
- Always use: FROM sales
- NEVER use sales_data or any other name
- For date use: strftime('%Y', order_date)

Examples:
Q: Total sales
A: SELECT SUM(sales) FROM sales;

Q: Profit by category
A: SELECT category, SUM(profit) FROM sales GROUP BY category;

Q: Yearly sales
A: SELECT strftime('%Y', order_date), SUM(sales) FROM sales GROUP BY strftime('%Y', order_date);

Now:
Q: {question}
A:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    return clean_sql(response.json()['response'])


def fix_sql(bad_sql, error):
    columns = get_schema()

    prompt = f"""
Fix this SQL query:

{bad_sql}

Error:
{error}

STRICT RULES:
- Return ONLY SQL
- Must use table: sales
- Use lowercase column names
- Must start with SELECT and end with ;

Table: sales
Columns: {', '.join(columns)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    return clean_sql(response.json()['response'])


def generate_insight(df):
    prompt = f"""
Give 2 short business insights from this data:

{df.to_string()}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    return response.json()['response']