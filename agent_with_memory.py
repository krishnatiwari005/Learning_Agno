import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.json import JsonDb
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()

llm = Groq(id="openai/gpt-oss-20b", api_key=api_key)

session_id = "my-session-id"
db = JsonDb(db_path="chat_historyDB",session_table="session_history")

agent = Agent(
    model=llm,
    name="my-agent-memory",
    markdown=True,
    add_history_to_context=True,
    num_history_runs=3,
    session_id=session_id,
    db=db,
    stream=True
)

agent.print_response(input="hi, my name is krishna.")
agent.print_response(input="what is my name?")
messages=agent.get_chat_history(session_id=session_id)
for message in messages:
    role,content=message.role,message.content
    if role=="system":
        continue
    else:
        print(f"{role}: {content}")