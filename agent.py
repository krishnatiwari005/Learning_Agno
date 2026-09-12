import os
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb

load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

db=SqliteDb(db_file="chat_history.db")

agent=Agent(
    name="my-agent",
    model=llm,
    markdown=True,
    stream=True,
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    session_id="session-1",
    user_id="user1"
)

agent.print_response(input="what is machine learning in 100 words?")
agent.print_response(input="what are we talking about right now?")