import matplotlib.pyplot as plt
import streamlit as st


def plot_chart(df):
    if df is None or df.empty:
        st.info("No data to visualize")
        return

    # 🔥 LIMIT rows (IMPORTANT)
    if len(df) > 50:
        st.warning("⚠️ Large dataset detected, showing top 50 rows for visualization")
        df = df.head(50)

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) == 0:
        st.info("No numeric columns available for chart")
        return

    try:
        x_col = df.columns[0]
        y_col = numeric_cols[0]

        if y_col not in df.columns:
            return

        plt.figure()

        if "date" in x_col.lower() or "year" in x_col.lower():
            df.plot(kind='line', x=x_col, y=y_col)
        else:
            df.plot(kind='bar', x=x_col, y=y_col)

        plt.xticks(rotation=45)
        st.pyplot(plt)

    except Exception as e:
        st.warning(f"Chart skipped: {str(e)}")