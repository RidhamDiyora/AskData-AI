import streamlit as st
from utils.llm import generate_sql, fix_sql, generate_insight, rewrite_question
from utils.db import load_uploaded_data, run_query
from utils.charts import plot_chart
from utils.safety import is_safe_query

st.set_page_config(page_title="AskData AI", layout="wide")

st.title("🤖 AskData AI")
st.write("Chat with your data using AI")

# Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])

if uploaded_file:
    table_name, columns, preview_df = load_uploaded_data(uploaded_file)

    st.success("Dataset uploaded!")

    st.dataframe(preview_df.head())

    # Show chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your data...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # 🧠 Rewrite question
        rewritten = rewrite_question(user_input, st.session_state.messages)

        if len(rewritten) < 5:
            rewritten = user_input

        st.write("🧠 Interpreted:", rewritten)

        sql = generate_sql(rewritten, table_name, columns)

        if is_safe_query(sql):
            try:
                df = run_query(sql)
            except Exception as e:
                sql = fix_sql(sql, str(e), table_name, columns)
                df = run_query(sql)

            with st.chat_message("assistant"):
                st.code(sql, language="sql")
                st.dataframe(df)

                if not df.empty:
                    plot_chart(df)
                    st.write(generate_insight(df))
                else:
                    st.warning("No results found")

            st.session_state.messages.append({
                "role": "assistant",
                "content": rewritten
            })