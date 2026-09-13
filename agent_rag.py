from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agent_knowledge import knowledge_base
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

agent = Agent(
    model=llm,
    name="my_knowledge_agent",
    markdown=True,
    stream=True,
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=["you are the helpfull assistant,whenever asked about constitution use the knowledge for the context","try not to hallucinate while responding ","if you dont know the answer to the particular query just say i dont know"]
)

agent.print_response("hi i am krishna  ")
agent.print_response("what is the key features of indian constitutional scheme")