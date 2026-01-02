import streamlit as st
from outreach_agent import run_outreach_task

# --- WEB PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Sales Agent", page_icon="🤖", layout="centered")

st.title("🤖 B2B Outreach Automation")
st.markdown("""
    This agent researches a company's current job openings and drafts a 
    personalized pitch for recruitment software.
""")

# --- SIDEBAR FOR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    # This looks for the key in Streamlit's secure cloud settings
if "GROQ_KEY" in st.secrets:
    user_api_key = st.secrets["GROQ_KEY"]
else:
    # Fallback: if secrets aren't set, show the sidebar input
    with st.sidebar:
        user_api_key = st.text_input("Groq API Key", type="password")

# --- MAIN INTERFACE ---
company = st.text_input("Target Company Name", placeholder="e.g., NVIDIA, Microsoft, Zomato")

if st.button("Generate Personalized Outreach"):
    if not user_api_key:
        st.error("❌ Please enter your Groq API Key in the sidebar!")
    elif not company:
        st.warning("⚠️ Please enter a company name.")
    else:
        with st.spinner(f"🕵️ Agent is researching {company}...."):
            try:
                # CALL THE ENGINE
                email_draft = run_outreach_task(company, user_api_key)
                
                st.success("✅ Research and Drafting Complete!")
                
                # DISPLAY THE RESULT
                st.subheader(f"Drafted Email for {company}")
                st.text_area("Final Output:", value=email_draft, height=400)
                
                # DOWNLOAD BUTTON
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