import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor

def run_outreach_task(company_name, api_key):
    """
    This function takes a company name and API key, 
    researches the company, and returns a drafted email.
    """
    # 1. Set the API Key dynamically
    os.environ["GROQ_API_KEY"] = api_key

    # 2. Initialize the LLM (Llama 3.3)
    llm = ChatGroq(
        temperature=0.7, 
        model_name="llama-3.3-70b-versatile"
    )

    # 3. Setup the Search Tool
    search_tool = DuckDuckGoSearchRun()

    # 4. Create the Agent Logic
    # Pulls the standard ReAct prompt from LangChain Hub
    try:
        prompt = hub.pull("hwchase17/react")
    except Exception as e:
        return f"Connection Error: Could not reach LangChain Hub. {e}"

    agent = create_react_agent(llm, [search_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

    # 5. Define the specific task
    task = f"Find out what {company_name} is currently hiring for and write a short, professional email to their HR manager proposing a new recruitment software."

    # 6. Execute and return the result
    result = agent_executor.invoke({"input": task})
    return result["output"]

# This allows you to still test this file alone by running 'python outreach_agent.py'
if __name__ == "__main__":
    test_key = "YOUR_GROQ_API_KEY_HERE" 
    print(run_outreach_task("SpaceX", test_key))