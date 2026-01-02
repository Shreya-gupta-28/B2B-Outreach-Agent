import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor

def run_outreach_task(company_name, user_goal, api_key):
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

    # DYNAMIC INSTRUCTION: We combine the company and the specific goal
    # This replaces the hardcoded recruitment text.
    instructions = (
        f"Research the company '{company_name}'. "
        f"Based on your research, write a professional B2B outreach email with this goal: {user_goal}. "
        "Do NOT mention recruitment software unless it is part of the goal."
    )

    # 6. Execute and return the result
    result = agent_executor.invoke({"input": instructions})
    return result["output"]

# This allows you to still test this file alone by running 'python outreach_agent.py'
if __name__ == "__main__":
    test_key = "YOUR_GROQ_API_KEY_HERE" 
    print(run_outreach_task("SpaceX", test_key))