import matplotlib.pyplot as plt
import streamlit as st


def plot_chart(df):
    if df is None or df.empty:
        st.info("No data to visualize")
        return

    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) == 0:
        st.info("No numeric columns available for chart")
        return

    # Safe column selection
    try:
        x_col = df.columns[0]

        # Pick first numeric column safely
        y_col = numeric_cols[0]

        if y_col not in df.columns:
            st.warning("Column mismatch, skipping chart")
            return

        plt.figure()

        # Smart chart selection
        if "date" in x_col.lower() or "year" in x_col.lower():
            df.plot(kind='line', x=x_col, y=y_col)
        else:
            df.plot(kind='bar', x=x_col, y=y_col)

        plt.xticks(rotation=45)
        st.pyplot(plt)

    except Exception as e:
        st.warning(f"⚠️ Chart skipped: {str(e)}")