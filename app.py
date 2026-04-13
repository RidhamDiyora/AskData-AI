import streamlit as st
from utils.llm import generate_sql, fix_sql, generate_insight, rewrite_question
from utils.db import load_uploaded_data, run_query
from utils.charts import plot_chart
from utils.safety import is_safe_query

st.set_page_config(
    page_title="AskData AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom Styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.stChatMessage {
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🧠 Header
st.title("🤖 AskData AI")
st.info("⚠️ This is an AI-powered prototype. Results may vary.")
st.caption("Chat with your data using AI-powered SQL analysis")

# 📂 Sidebar
with st.sidebar:
    st.header("📂 Upload Dataset")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    st.divider()

    st.subheader("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

    st.divider()

    st.subheader("ℹ️ Tips")
    st.write("""
- Ask clear questions  
- Use column names  
- Try: "sales by year"  
- Try: "top 5 products"  
""")

# 💬 Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📊 Main logic
if uploaded_file:
    table_name, columns, preview_df = load_uploaded_data(uploaded_file)

    st.success("✅ Dataset uploaded successfully")

    # 📊 Preview
    with st.expander("📊 Preview Data"):
        st.dataframe(preview_df.head(), width="stretch")

    # 📋 Columns
    with st.expander("📋 Columns"):
        st.write(columns)

    # 💬 Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 💬 Chat input
    user_input = st.chat_input("Ask your data like ChatGPT...")

    if user_input:
        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # 🧠 Rewrite question
        rewritten = rewrite_question(user_input, st.session_state.messages)

        if len(rewritten.strip()) < 5:
            rewritten = user_input

        with st.chat_message("assistant"):
            st.markdown(f"🧠 *Interpreted:* {rewritten}")

        # 🔍 Generate SQL
        try:
            sql = generate_sql(rewritten, table_name, columns)
        except Exception:
            st.error("⚠️ Ollama is not running. Run: ollama serve")
            st.stop()

        # 🛡️ Validate SQL
        if not sql.upper().startswith("SELECT"):
            st.error("Invalid SQL generated")
            st.stop()

        if is_safe_query(sql):
            try:
                df = run_query(sql, table_name, columns)
            except Exception as e:
                st.warning("⚠️ Fixing query...")
                sql = fix_sql(sql, str(e), table_name, columns)
                df = run_query(sql, table_name, columns)

            # 💬 Assistant output
            with st.chat_message("assistant"):
                st.code(sql, language="sql")

                st.dataframe(df, width="stretch")

                if df.empty:
                    st.warning("⚠️ No results found. Try rephrasing.")
                else:
                    st.markdown("### 📈 Visualization")
                    plot_chart(df)

                    st.markdown("### 🧠 Insights")
                    st.write(generate_insight(df))

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": rewritten
            })

        else:
            st.error("Unsafe query detected")

# ❌ No dataset
else:
    st.info("📂 Upload a dataset to start chatting with your data")