from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.team import Team
from dotenv import load_dotenv
import os 

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

news_agent=Agent(
    id="news_agent",
    name="News Agent",
    model=llm,
    role="Give the latest news headlines and head summary",
    instructions=["You are the news search agent ",
                  "Search for the latest news for the particular destination and give the summarized view"],
    tools=[DuckDuckGoTools()]
)

web_search_agent=Agent(
    id="web_search_agent",
    name="Web search Agent",
    model=llm,
    role="Get information for the places to visit at the destination",
    instructions=["you are the web search agent",
                  "Your goal is to search for places of interest for a particular destination"],
    tools=[DuckDuckGoTools()]
)

travel_agent=Team(
    members=[news_agent,web_search_agent],
    name="Travel agent",
    id="travel_agent",
    model=llm,
    role="You are the team leader and you delegate the tasks to others member",
    instructions=["You are the expert travel agent",
                  "Your team members could get the latest news and search for the places of interest for the particular destination",
                  "your task is to present the output using proper headlines"],
    stream=True,
    markdown=True,
)

travel_agent.cli_app(stream=True,markdown=True)