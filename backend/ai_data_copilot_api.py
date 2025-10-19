from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import pandas as pd
import json
import re
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

# Allow Power BI / Streamlit access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#client = OpenAI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        df = pd.DataFrame(data)

        if df.empty:
                return {"error": "Dataset is empty or invalid"}

        # Build a compact data summary for AI context
        summary = df.describe(include='all').head(5).to_string()

        prompt = f"""
        You are a senior data analyst AI.
        Analyze the dataset below and provide:
        1. 3–5 key insights or trends.
        2. Recommended visualizations with column mappings.
        Dataset summary:
        {summary}
        Respond strictly in JSON format:
        {{
        "insights": ["...", "...", "..."],
        "charts": [
            {{"type": "bar", "x": "Region", "y": "Sales"}},
            {{"type": "line", "x": "Month", "y": "Revenue"}}
        ]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        try:
            # output = response.choices[0].message.content
            # result = json.loads(output)
            output = response.choices[0].message.content.strip()

            # Clean up Markdown code block formatting if present
            if output.startswith("```"):
                output = output.split("```json")[-1].split("```")[-1].strip()
                output = output.replace("```", "").strip()

            result = json.loads(output)
            
        except Exception:
            result = {
                "insights": [response.choices[0].message.content],
                "charts": []
            }

        return result
    except Exception as e:
        return {"error": str(e)}