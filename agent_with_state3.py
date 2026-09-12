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

session_id="sessionC"
user_id="userC"

def add_items(run_context:RunContext,item:str) -> str:
    """Add an item to the shopping list"""
    item=item.lower()
    shopping_list=run_context.session_state["shopping_list"]
    if item in shopping_list:
        return f"{item} is already in the shopping list"
    else:
        shopping_list.append(item)
        return f"{item} has been added to the shopping list"

def remove_items(run_context:RunContext,item:str) -> str:
    """Remove an item from the shopping list"""
    item=item.lower()
    shopping_list=run_context.session_state["shopping_list"]
    if item in shopping_list:
        shopping_list.remove(item)
        return f"{item} has been removed from the shopping list"
    else:
        return f"{item} is not in the shopping list"

def list_items(run_context:RunContext,item:str="")->str:
    """List down all the items in the list"""
    shopping_list=run_context.session_state["shopping_list"]
    if shopping_list:
        list_of_items="\n".join([f"- {item}" for item in shopping_list])
        return f"Here are the items in the shopping list:\n{list_of_items}"
    else:
        return "The shopping list is empty."

def clear_list(run_context:RunContext,item:str="")->str:
    """Clear the shopping list"""
    shopping_list=run_context.session_state["shopping_list"]
    shopping_list.clear()
    return "The shopping list has been cleared."

agent=Agent(
    model=llm,
    db=db,
    stream=True,
    session_state={"shopping_list":[]},
    instructions="your are expert in managing the shopping list and here you can add, remove and read and clear all the item in the shopping list ",
    name="agent_with_state",
    markdown=True,
    tools=[add_items, remove_items, list_items, clear_list],
    session_id=session_id,
    user_id=user_id
)

agent.print_response("add milk to the list")
print(f"the session state is {agent.get_session_state(session_id)}")

agent.print_response("add bread and curd to the list")
print(f"the session state is {agent.get_session_state(session_id)}")

agent.print_response("remove milk from the list")
print(f"the session state is {agent.get_session_state(session_id)}")

agent.print_response("list all items in the list")
print(f"the session state is {agent.get_session_state(session_id)}")

agent.print_response("clear the shopping list")
print(f"the session state is {agent.get_session_state(session_id)}")