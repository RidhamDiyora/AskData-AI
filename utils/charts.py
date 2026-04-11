import matplotlib.pyplot as plt
import streamlit as st


def plot_chart(df):
    if df.empty:
        return

    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        st.info("No numeric data to visualize")
        return

    x_col = df.columns[0]
    y_col = numeric_cols[0]

    plt.figure()

    # Smart chart selection
    if "date" in x_col or "year" in x_col:
        df.plot(kind='line', x=x_col, y=y_col)
    else:
        df.plot(kind='bar', x=x_col, y=y_col)

    plt.xticks(rotation=45)
    st.pyplot(plt)