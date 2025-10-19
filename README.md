# 🤖 AI Data Copilot

AI-powered assistant that turns your Excel/CSV data into actionable insights using OpenAI GPT.

---

## 🚀 Features
- Upload Excel or CSV files
- Auto-summary using GPT-4o-mini
- Visualize numeric columns
- Easy Streamlit deployment

---

## 🛠️ Setup

```bash
git clone https://github.com/vrajans/ai_data_copilot.git
cd ai_data_copilot
pip install -r requirements.txt
cp .env.template .env
# Add your OpenAI key in .env
streamlit run app.py