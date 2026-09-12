from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from agno.run import RunContext
import os
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

web_search_tool=DuckDuckGoTools()

agent=Agent(
    model=llm,
    name="agent_with_tool",
    tools=[web_search_tool],
    instructions="you are expert in searching the web and you have access to the tool called DuckDuckGoTools which can search the web and return the result to you, you can use this tool to search the web and get the information you need",
    stream=True,
    markdown=True,
)

agent.print_response("Search for latest news in India", stream=True)