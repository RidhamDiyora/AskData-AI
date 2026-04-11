# 🤖 AskData AI

AI-powered data analyst using local LLM (Ollama + Llama3)

## 🚀 Features
- Natural Language → SQL
- Local LLM (no API cost)
- Auto visualization
- AI-generated insights
- SQL safety layer

## 🛠 Tech Stack
- Python
- Streamlit
- SQLite
- Ollama (Llama3)

## ▶️ Run

```bash
pip install -r requirements.txt
ollama serve
ollama pull llama3
python load_data.py
streamlit run app.py