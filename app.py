import streamlit as st
from utils.llm import generate_sql, generate_insight, fix_sql
from utils.db import run_query
from utils.safety import is_safe_query
from utils.charts import plot_chart

st.set_page_config(page_title="AskData AI", layout="wide")

st.title("🤖 AskData AI")
st.write("Your AI-powered data analyst (Local LLM)")

question = st.text_input("🔍 Ask a question about your data:")

show_sql = st.checkbox("Show SQL Query")

if question:
    try:
        with st.spinner("Thinking..."):
            sql = generate_sql(question)
    except Exception:
        st.error("⚠️ Ollama is not running. Run: ollama serve")
        st.stop()

    # ✅ Validate SQL structure
    if not sql.upper().startswith("SELECT"):
        st.error("❌ Invalid SQL generated. Try rephrasing.")
        st.stop()

    # ✅ Ensure correct table
    if "sales" not in sql.lower():
        st.error("❌ Invalid table used. Only 'sales' allowed.")
        st.stop()

    if show_sql:
        st.code(sql, language="sql")

    if is_safe_query(sql):
        try:
            df = run_query(sql)

        except Exception as e:
            st.warning("⚠️ Fixing query...")

            sql = fix_sql(sql, str(e))

            if show_sql:
                st.code(sql, language="sql")

            df = run_query(sql)

        st.subheader("📊 Results")
        st.dataframe(df)

        if not df.empty:
            st.subheader("📈 Visualization")
            plot_chart(df)

            st.subheader("🧠 Insights")
            st.write(generate_insight(df))
        else:
            st.warning("No data returned.")

    else:
        st.error("Unsafe query detected!")