from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from agno.run import RunContext
import os
load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

db=SqliteDb(db_file="Session_state_db/shopping.db")

session_id="sessionB"
user_id="userB"

def add_items(run_context:RunContext,item:str) -> str:
    """Add an item to the shopping list"""
    shopping_list=run_context.session_state["shopping_list"]
    shopping_list.append(item)
    return f"shopping list is now{run_context.session_state['shopping_list']}"

agent=Agent(
    model=llm,
    db=db,
    stream=True,
    session_state={"shopping_list":[]},
    instructions="you are expert in maintaining shopping list and you have access to the shopping list{shopping_list}",
    name="agent_with_state",
    markdown=True,
    tools=[add_items],
    session_id=session_id,
    user_id=user_id
)

agent.print_response("add milk to the list")
print(f"the session state is {agent.get_session_state(session_id)}")

agent.print_response("add bread and curd to the list")
print(f"the session state is {agent.get_session_state(session_id)}")
