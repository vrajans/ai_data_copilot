from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = FastAPI(title="AI Data Copilot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.post('/analyze')
async def analyze(file: UploadFile = File(...), question: str = ""):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents)) if file.filename.endswith('.csv') else pd.read_excel(io.BytesIO(contents))
        schema = f"Columns: {', '.join(df.columns)}\n\n" + str(df.describe(include='all'))
        prompt = f"You are a helpful data analyst. Given the dataset summary:\n{schema}\n\nQuestion: {question}\nProvide concise, actionable insights and 3 recommended next steps."
        resp = client.chat.completions.create(model='gpt-4o-mini', messages=[{"role":"user","content":prompt}], max_tokens=700)
        return {"insights": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))