# import streamlit as st
# import pandas as pd
# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# import matplotlib.pyplot as plt
# from utils.data_utils import summarize_dataframe

# # Load environment variables
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Streamlit App UI
# st.set_page_config(page_title="AI Data Copilot", layout="wide")
# st.title("🤖 AI Data Copilot")
# st.markdown("Upload your Excel or CSV file and let AI summarize your business insights!")

# uploaded_file = st.file_uploader("📂 Upload Excel or CSV", type=["csv", "xlsx"])

# if uploaded_file:
#     try:
#         # Read uploaded file
#         if uploaded_file.name.endswith(".csv"):
#             df = pd.read_csv(uploaded_file)
#         else:
#             df = pd.read_excel(uploaded_file)

#         st.success("✅ File uploaded successfully!")
#         st.dataframe(df.head())

#         # Generate data summary
#         with st.spinner("Generating AI insights..."):
#             stats_summary = summarize_dataframe(df)
#             prompt = f"Analyze the following summary and generate clear, actionable business insights:\n{stats_summary}"

#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[{"role": "user", "content": prompt}]
#             )
#             insights = response.choices[0].message.content

#         st.subheader("📊 AI Insights")
#         st.write(insights)

#         # Visualization example
#         st.subheader("📈 Sample Chart")
#         numeric_cols = df.select_dtypes(include=["number"]).columns
#         if len(numeric_cols) >= 1:
#             fig, ax = plt.subplots()
#             df[numeric_cols[0]].head(10).plot(kind="bar", ax=ax, color="#4CAF50")
#             ax.set_title(f"Sample Chart of {numeric_cols[0]}")
#             st.pyplot(fig)

#         # Future feature: Email the report
#         st.info("📧 Coming soon: Automated email report generation.")

#     except Exception as e:
#         st.error(f"Error processing file: {e}")

import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from utils.data_utils import summarize_dataframe
from utils.chart_utils import render_chart

from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="AI Data Copilot", layout="wide")
st.title("🤖 AI Data Copilot")
st.markdown("Upload a CSV/XLSX or connect to a database and let AI generate insights and charts.")

uploaded_file = st.file_uploader("📂 Upload Excel or CSV", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        #st.subheader("📊 Data Summary")
        #st.text(summarize_dataframe(df))

        st.subheader("Ask the AI about your data")
        question = st.text_input("e.g., 'Which region has the highest sales?'")

        if st.button("Generate Insight") and question:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            schema = summarize_dataframe(df)

            prompt = f"""
            You are a data analysis assistant.
            Given this dataset summary:
            {schema}

            User question: {question}

            Provide:
            1. A short natural language insight (2–3 sentences)
            2. A JSON block suggesting an appropriate chart, e.g.:
            {{"chart_type": "bar", "x": "region", "y": "sales", "aggregation": "sum"}}
            """

            with st.spinner('Generating insights...'):
                try:
                    response = client.chat.completions.create(
                        model='gpt-4o-mini',
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=800
                    )

                    insights = response.choices[0].message.content
                    st.subheader('🧠 AI Insights')
                    text_part = insights.split('```json')[0].strip()
                    st.write(text_part)

                    # Attempt to extract chart spec
                    try:
                        json_part = insights.split('```json')[1].split('```')[0]
                        chart_spec = json.loads(json_part)
                        render_chart(df, chart_spec)
                    except Exception as ce:
                        st.info("No valid chart specification found in AI response.")

                except Exception as e:
                    st.error(f'AI request failed: {e}')

    except Exception as e:
        st.error(f"Error processing file: {e}")