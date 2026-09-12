import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()

llm = Groq(id="openai/gpt-oss-20b", api_key=api_key)

user_id="user-123"
db = SqliteDb(db_file="chat_historyDB/demo.db")

agent = Agent(
    model=llm,
    name="my-agent-memory",
    markdown=True,
    add_history_to_context=True,
    num_history_runs=3,
    db=db,
    stream=True
)
session_transformer="session-transformer"
session_rag="session-rag"

agent.print_response(input="hi, can u tell about transformers in 50 words?",session_id=session_transformer)
agent.print_response(input="hi, can u tell about self attention in 50 words?",session_id=session_transformer)
agent.print_response(input="hi, can u tell about rag in 50 words?",session_id=session_rag)
agent.print_response(input="hi, can u tell about retriever in 50 words?",session_id=session_rag)
print()
print()

print("==============transformer session history===================")
messages=agent.get_chat_history(session_id=session_transformer)
for message in messages:
    role,content=message.role,message.content
    if role=="system":
        continue
    else:
        print(f"{role}: {content}")


print("==============rag session history===================")
messages=agent.get_chat_history(session_id=session_rag)
for message in messages:
    role,content=message.role,message.content
    if role=="system":
        continue
    else:
        print(f"{role}: {content}")
