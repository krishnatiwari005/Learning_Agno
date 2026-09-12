from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
import os
load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

db=SqliteDb(db_file="Session_state_db/demo.db")

session_id="sessionA"
user_id="userA"

user_info={
    "name":"Krishna tiwari",
    "age":23
}
agent=Agent(
    model=llm,
    db=db,
    stream=True,
    session_state=user_info,
    add_session_state_to_context=True,
    name="agent_with_state",
    markdown=True,
    session_id=session_id,
    user_id=user_id
)

# agent.print_response(input="hi what is my name and age?",session_state={"name":"neha","age":88})
print(agent.get_session_state(session_id=session_id))