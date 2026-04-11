import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plot_chart(df):
    if df.empty:
        st.warning("No data to plot.")
        return

    # Detect numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        st.info("📊 No numeric data available for visualization.")
        return

    # Use first column as x-axis
    x_col = df.columns[0]
    y_col = numeric_cols[0]

    try:
        plt.figure()
        df.plot(kind='bar', x=x_col, y=y_col)
        plt.xticks(rotation=45)
        st.pyplot(plt)
    except Exception as e:
        st.warning(f"Could not generate chart: {e}")