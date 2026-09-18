from agno.agent import Agent
from agno.models.groq import Groq
from agno.workflow import Workflow,Step,Loop,StepOutput,Condition,StepInput,Router
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

def is_tech_topic(step_input:StepInput)->list[Step]:
    """condition to check whether the input topic is technical or not """
    tech_keywords=["technology","tech","ai","Machine Learning", "computer","internet","hardware","gadgets","electronics","Artificial intelligence"]
    user_input=step_input.input or ""
    if user_input:
        user_input=user_input.lower()
        if any(keyword in user_input for keyword in tech_keywords):
            return [hackernews_search_step]
        else:
            return [duckduckgo_search_step]


duckduckgo_search_agent=Agent(
    id="duckduckgo-agent",
    name="duckduckgo search Agent ",
    model=llm,
    tools=[DuckDuckGoTools()],
    instructions=["you are an expert web search agent",
                  "Provide relevant and accurate information based on user's query"],
)

hackernews_search_agent=Agent(
    id="hackernews-agent",
    name="Hackernews search Agent ",
    model=llm,
    tools=[HackerNewsTools()],
    instructions=["you are an expert agent",
                  "you retreive relevant and latest news from hackernews platform"],
)

content_creation_agent=Agent(
    id="content-creation-agent",
    name="Content creation Agent",
    model=llm,
    instructions=["you are expert in content creation and writing articles",
                  "you take in research data and create engaging well structured article",
                  "format the content with proper heading ,bullet points and clear conclusion"]
)

duckduckgo_search_step=Step(
    name="Duck Duck GO search step",
    agent=duckduckgo_search_agent,
    description="performs web search using duckduckgo search"
)

hackernews_search_step=Step(
    name="Hackernews search step",
    agent=hackernews_search_agent,
    description="retreive latest news and trending topic using hackernews search"
)

content_creation_step=Step(
    name="Content creation step",
    agent=content_creation_agent,
    description="creates engaging article based on data provided"
)

router_step=Router(
    name="Topic router step",
    description="routes the workflow based on whether the topic is tech based or not",
    choices=[duckduckgo_search_step,hackernews_search_step],
    selector=is_tech_topic,
)

workflow=Workflow(
    id="Research-and-create-workflow",
    name="Reserch and publish article workflow",
    steps=[router_step,content_creation_step],
    description="A workflow that researches a topic from different sources based on if the topic is tech related or not and write an engaging article based on research "
)

workflow.print_response(input="create and article about AI",stream=True,markdown=True)
