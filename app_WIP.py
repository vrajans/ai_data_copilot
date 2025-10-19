import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from utils.data_utils import summarize_dataframe

load_dotenv()

st.set_page_config(page_title="AI Data Copilot", layout="wide")
st.title("🤖 AI Data Copilot")
st.markdown("Upload a CSV/XLSX or connect to a database and let the AI generate insights.")

uploaded_file = st.file_uploader("📂 Upload Excel or CSV", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        st.subheader("📊 Data Summary")
        st.text(summarize_dataframe(df))

        st.subheader("Ask the AI about your data")
        question = st.text_input("What would you like to ask? e.g. 'Top 3 reasons for drop in sales?'")
        if st.button("Generate Insight") and question:

            # Minimal local prompt creation - send only summary, schema and question to OpenAI
            import os
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            schema = summarize_dataframe(df)
            prompt = f"You are a helpful data analyst. Given the dataset summary:\n{schema}\n\nQuestion: {question}\nProvide concise, actionable insights and 3 recommended next steps."
            with st.spinner('Generating insights...'):
                try:
                    response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=600
                    )
                    insights = response.choices[0].message.content
                    st.subheader('🧠 AI Insights')
                    st.write(insights)
                except Exception as e:
                    st.error(f'AI request failed: {e}')
    except Exception as e:
        st.error(f"Error processing file: {e}")