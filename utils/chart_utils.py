import streamlit as st
import pandas as pd

def render_chart(df: pd.DataFrame, chart_spec: dict):
    st.subheader("📈 Visualization")
    chart_type = chart_spec.get("chart_type", "bar")
    x = chart_spec.get("x")
    y = chart_spec.get("y")
    agg = chart_spec.get("aggregation", "sum")

    if not x or not y:
        st.warning("Chart specification missing 'x' or 'y'.")
        return

    try:
        if agg == 'sum':
            grouped = df.groupby(x)[y].sum().reset_index()
        elif agg == 'mean':
            grouped = df.groupby(x)[y].mean().reset_index()
        else:
            grouped = df.groupby(x)[y].count().reset_index()

        if chart_type == 'bar':
            st.bar_chart(grouped, x=x, y=y)
        elif chart_type == 'line':
            st.line_chart(grouped, x=x, y=y)
        elif chart_type == 'area':
            st.area_chart(grouped, x=x, y=y)
        elif chart_type == 'scatter':
            st.scatter_chart(grouped, x=x, y=y)
        else:
            st.write(f"Unsupported chart type: {chart_type}")

    except Exception as e:
        st.warning(f"Chart rendering failed: {e}")