import streamlit as st
from outreach_agent import run_outreach_task

# --- WEB PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Sales Agent", page_icon="🤖", layout="centered")

st.title("🤖 B2B Outreach Automation")
st.markdown("""
    This agent researches a company's current job openings and drafts a 
    personalized pitch for recruitment software.
""")

# --- API KEY LOGIC (FIXED INDENTATION) ---
# 1. First, check if the key is in Streamlit Cloud Secrets
if "GROQ_KEY" in st.secrets:
    user_api_key = st.secrets["GROQ_KEY"]
else:
    # 2. If not found in Secrets, show the sidebar input as a fallback
    with st.sidebar:
        st.header("Settings")
        user_api_key = st.text_input("Groq API Key", type="password", help="Enter your key here if not set in Cloud Secrets")
        if not user_api_key:
            st.warning("Please enter your Groq API Key to proceed.")

# --- MAIN INTERFACE ---
company = st.text_input("Target Company Name", placeholder="e.g., NVIDIA, Microsoft, Zomato")

if st.button("Generate Personalized Outreach"):
    if not user_api_key:
        st.error("❌ API Key not found! Please add it to 'Advanced Settings' on Streamlit Cloud or the sidebar.")
    elif not company:
        st.warning("⚠️ Please enter a company name.")
    else:
        with st.spinner(f"🕵️ Agent is researching {company}...."):
            try:
                # The agent uses the key discovered above
                email_draft = run_outreach_task(company, user_api_key)
                
                st.success("✅ Research and Drafting Complete!")
                st.subheader(f"Drafted Email for {company}")
                st.text_area("Final Output:", value=email_draft, height=400)
                
                st.download_button(
                    label="📥 Download Email (.txt)",
                    data=email_draft,
                    file_name=f"{company}_outreach.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()
st.caption("Powered by LangChain + Groq + Llama 3.3")