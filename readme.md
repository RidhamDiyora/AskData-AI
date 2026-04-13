# 🤖 AskData AI

Ask questions about your dataset in natural language and get instant insights, SQL queries, and visualizations.

---

## 🚀 Live Demo

👉 https://askdata-ai-5m2f4npzeh9kw7kq23hupk.streamlit.app/

---

## 💡 Overview

**AskData AI** is an AI-powered data analysis tool that allows users to:

* Upload any CSV dataset 📂
* Ask questions in plain English 💬
* Automatically generate SQL queries 🧠
* Visualize results with charts 📊
* Get AI-generated insights 💡

---

## ✨ Features

* 🔍 Natural Language → SQL conversion
* 🧠 AI-powered query correction (self-healing SQL)
* 📊 Automatic chart generation
* 💡 Smart insights generation
* 📂 Works with any uploaded dataset
* ⚡ Fast inference using Groq LLM
* 🛡 Handles large datasets with aggregation

---

## 🧠 How It Works

1. Upload a dataset (CSV)
2. Ask a question (e.g., "students by gender")
3. AI converts it into SQL
4. Query runs on SQLite
5. Results + chart + insights are displayed

---

## 🛠 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** SQLite
* **LLM:** Groq (LLaMA 3)
* **Visualization:** Matplotlib / Pandas

---

## ⚠️ Disclaimer

This is an AI-powered prototype.
Results may not always be accurate — please verify important insights.

---

## 🧪 Example Questions

* "Total students"
* "Students by gender"
* "Average usage hours"
* "Top 5 categories"

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/askdata-ai.git
cd askdata-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🔑 Setup

Create a `.env` or add Streamlit secrets:

```
GROQ_API_KEY=your_api_key
```

---

## ▶️ Run App

```bash
streamlit run app.py
```

---

## 💼 Why This Project?

This project demonstrates:

* LLM integration with real-world data
* Prompt engineering & error handling
* SQL generation + correction
* End-to-end data pipeline
* Deployment-ready AI application

---

## 🚀 Future Improvements

* Multi-dataset support
* Dashboard builder
* Export insights (PDF/CSV)
* User authentication
