# 🤖 Agentic B2B Outreach Researcher
An autonomous AI Agent that researches companies and drafts personalized sales outreach using Llama 3.3 and LangChain.

## 🚀 How it Works
1. **Research:** The agent uses DuckDuckGo to find real-time job openings for a target company.
2. **Reasoning:** Using a ReAct (Reasoning + Acting) loop, it analyzes the data to find pain points.
3. **Drafting:** It generates a professional B2B email tailored to the company's specific hiring needs.

## 🛠️ Tech Stack
- **Model:** Llama 3.3 70B (via Groq)
- **Framework:** LangChain & LangGraph
- **UI:** Streamlit
- **Search:** DuckDuckGo

## ⚙️ Setup
1. Clone this repo.
2. Install requirements: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`