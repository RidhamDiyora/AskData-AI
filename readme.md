# 🤖 AskData AI

**AskData AI** is an AI-powered data analyst that converts natural language questions into SQL queries using a local LLM and generates insights with visualizations — all running locally with no API cost.

---

## 🚀 Features

* 🧠 Natural Language → SQL (LLM-powered)
* 📊 Automatic Data Visualization
* 🔍 AI-generated Business Insights
* 🛡️ SQL Validation & Safety Layer
* 🔁 Auto Error Correction (fixes broken queries)
* 💻 Fully local (powered by Ollama + Llama3)

---

## 🛠 Tech Stack

* Python
* Streamlit
* SQLite
* Ollama (Llama3)
* Pandas
* Matplotlib

---
## 📁 Project Structure

```
askdata-ai/
│── app.py
│── load_data.py
│── requirements.txt
│── README.md
│── db/
│── data/
│── utils/
```

---

## ▶️ Run Locally

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start local LLM
ollama serve
ollama pull llama3

# 4. Load dataset
python load_data.py

# 5. Run app
streamlit run app.py
```

---

## 💡 Example Queries

* Total sales by region
* Monthly sales trend
* Least profitable category
* Yearly profit analysis
* Highest sales product

---

## 🧠 Key Highlights

* Built a full-stack AI application using a local LLM
* Implemented natural language to SQL conversion pipeline
* Designed SQL validation and auto-correction system
* Handled LLM limitations with schema enforcement and cleaning
* Created dynamic visualization layer for insights

---

## 💼 Why This Project Matters

This project demonstrates:

* Real-world LLM integration
* Strong SQL and data analysis skills
* Handling of unreliable AI outputs (production mindset)
* End-to-end application development

