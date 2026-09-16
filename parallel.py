from agno.models.groq import Groq
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow import Step,Workflow,Parallel
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

google_agent=Agent(
    id="google_agent",
    name="Google search agent",
    instructions=["you are an expert web search agent using web search",
                  "provide accurate and relevant information based on user query"],
    model=llm,
    tools=[WebSearchTools()]
)

duckduckgo_agent=Agent(
    id="duckduckgo_agent",
    name="Duck Duck go agent",
    instructions=["you are an expert web search agent using duckduckgo search",
                  "provide accurate and relevant information based on user query"],
    model=llm,
    tools=[DuckDuckGoTools()]
)

hackernews_agent=Agent(
    id="hackernews_agent",
    name="hacker news agent",
    instructions=["you are an expert in retreiving trending topic and latest news from hackernews "],
    model=llm,
    tools=[HackerNewsTools()]
)

report_generation_agent=Agent(
    id="report_generation_agent",
    name="report generation table",
    model=llm,
    instructions=["you are an expert in report generation",
                  "compile all the information from all the sources into a coherent and comprehensive report",
                  "output should be in a proper format"],
    markdown=True
)

google_search_step=Step(
    name="Google Search Step",
    agent=google_agent,
    description="perform a websearch using websearch"
)

duckduckgo_search_step=Step(
    name="DuckDuckGo Search Step",
    agent=duckduckgo_agent,
    description="perform a duckduckgo search using duckduckgo search"
)

hackernews_search_step=Step(
    name="hackernews Search Step",
    agent=hackernews_agent,
    description="perform a latest news search using hackernews search"
)

report_generation_step=Step(
    name="Report generation step",
    agent=report_generation_agent,
    description="generate a report compiling information gathered from various sources"
)

parallel_step=Parallel(
    google_search_step,
    duckduckgo_search_step,
    hackernews_agent,
    name="Parallel search step",
    description="perform searches from various sources parallely"
)

parallel_workflow=Workflow(
    id="parallel-workflow",
    name="retreiver and report generation",
    steps=[parallel_step,report_generation_step],
    description="A workflow that perform websearching using multiple agent parallely and then generate a report based on the retreived information "
)

parallel_workflow.print_response(input="topic: Agentic Ai",stream=True,markdown=True)