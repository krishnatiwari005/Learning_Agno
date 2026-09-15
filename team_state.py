from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from agno.run import RunContext
import os 


load_dotenv()


api_key=os.getenv("GROQ_API_KEY","").strip()


llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)


db=SqliteDb(db_file="test_db/demo.db",session_table="session_table")



def add_items(run_context:RunContext,list_name:str,item_name:str)->str:
    """Add item to the specified list"""

    item_name=item_name.lower().strip()
    list_name=list_name.lower().strip()

    valid_lists=["groceries_list","todo_list","study_list"]

    if list_name not in valid_lists:
        return f"Invalid list name: {list_name}"

    if list_name not in run_context.session_state:
        run_context.session_state[list_name]=[]

    run_context.session_state[list_name].append(item_name)

    return f"the item {item_name} added to the {list_name}"



def remove_items(run_context:RunContext,list_name:str,item_name:str)->str:
    """remove only the specified item from the specified list"""

    item_name=item_name.lower().strip()
    list_name=list_name.lower().strip()

    valid_lists=["groceries_list","todo_list","study_list"]

    if list_name not in valid_lists:
        return f"Invalid list name: {list_name}"

    if list_name not in run_context.session_state:
        run_context.session_state[list_name]=[]

    if item_name not in run_context.session_state[list_name]:
        return f"the item {item_name} is not present in the list {list_name}"

    run_context.session_state[list_name].remove(item_name)

    return f"the item {item_name} removed from the list {list_name}"



def list_items(run_context:RunContext,list_name:str)->str:
    """list item in the specified list"""

    list_name=list_name.lower().strip()

    valid_lists=["groceries_list","todo_list","study_list"]

    if list_name not in valid_lists:
        return f"Invalid list name: {list_name}"

    if list_name not in run_context.session_state:
        run_context.session_state[list_name]=[]

    if not run_context.session_state[list_name]:
        return f"the {list_name} is currently empty"

    text="\n".join([f"-{item}" for item in run_context.session_state[list_name]])

    return f"the item in the {list_name} are\n{text}"



def clear_list(run_context:RunContext,list_name:str)->str:
    """clear the specified list of all the items"""

    list_name=list_name.lower().strip()

    valid_lists=["groceries_list","todo_list","study_list"]

    if list_name not in valid_lists:
        return f"Invalid list name: {list_name}"

    if list_name not in run_context.session_state:
        run_context.session_state[list_name]=[]

    run_context.session_state[list_name].clear()

    return f"list {list_name} cleared of all the item"



def list_all_items(run_context:RunContext)->str:
    """list all items from all the personal lists"""

    groceries_list=run_context.session_state.get("groceries_list",[])
    todo_list=run_context.session_state.get("todo_list",[])
    study_list=run_context.session_state.get("study_list",[])

    groceries_text="\n".join([f"-{item}" for item in groceries_list])
    todo_text="\n".join([f"-{item}" for item in todo_list])
    study_text="\n".join([f"-{item}" for item in study_list])

    if not groceries_text:
        groceries_text="-Empty"

    if not todo_text:
        todo_text="-Empty"

    if not study_text:
        study_text="-Empty"

    return f"""
Groceries List:
{groceries_text}

Todo List:
{todo_text}

Study List:
{study_text}
"""



grocery_agent=Agent(
    id="grocery_agent",
    name="Grocery Agent",
    role="Manages list of the item in the Grocery List",
    instructions=["You are expert in managing grocery list",
                  "You manage only the groceries_list",
                  "You can add or remove item in the grocery list",
                  "You can list all the item in the grocery list",
                  "You can clear the grocery list if asked for",
                  "Always use groceries_list when calling a tool",
                  "Do not manage todo_list or study_list"],
    model=llm,
    db=db,
    tools=[add_items,remove_items,list_items,clear_list],
    add_session_state_to_context=True
)



todo_list_agent=Agent(
    id="todo_agent",
    name="todo list Agent",
    role="Manages list of the item in the todo List",
    instructions=["You are expert in managing todo list",
                  "You manage only the todo_list",
                  "You can add or remove item in the todo list",
                  "You can list all the item in the todo list",
                  "You can clear the todo list if asked for",
                  "Always use todo_list when calling a tool",
                  "Do not manage groceries_list or study_list"],
    model=llm,
    db=db,
    tools=[add_items,remove_items,list_items,clear_list],
    add_session_state_to_context=True
)



study_list_agent=Agent(
    id="study_agent",
    name="study list Agent",
    role="Manages list of the item in the study List",
    instructions=["You are expert in managing study list",
                  "You manage only the study_list",
                  "You can add or remove item in the study list",
                  "You can list all the item in the study list",
                  "You can clear the study list if asked for",
                  "Always use study_list when calling a tool",
                  "Do not manage groceries_list or todo_list"],
    model=llm,
    db=db,
    tools=[add_items,remove_items,list_items,clear_list],
    add_session_state_to_context=True
)



list_manager = Team(
    name="personal list manager",

    members=[
        grocery_agent,
        todo_list_agent,
        study_list_agent
    ],

    role="You are the central personal list manager. You understand the user's request, identify the correct list automatically, and delegate the operation to the appropriate specialist agent.",

    instructions=[
        # Core behavior
        "Always understand the user's intent before delegating the task.",
        "NEVER ask the user which list to use when the item or task clearly indicates the correct list.",
        "Automatically determine whether the request belongs to groceries_list, todo_list, or study_list.",

        # Available lists
        "There are exactly three lists:",
        "1. groceries_list - contains food, beverages, household shopping items, and things the user wants to buy.",
        "2. todo_list - contains general tasks, work, personal tasks, appointments, reminders, and things the user needs to do.",
        "3. study_list - contains study-related subjects, topics, chapters, courses, exams, assignments, and learning tasks.",

        # Grocery classification
        "Food items and shopping items normally belong to groceries_list.",
        "Examples: milk, bread, eggs, rice, vegetables, fruits, mango, banana, apples, toothpaste, soap, shampoo, coffee.",
        "If the user says 'add milk', use groceries_list.",
        "If the user says 'buy eggs', use groceries_list.",
        "If the user says 'add mango', use groceries_list.",
        "If the user says 'add banana', use groceries_list.",

        # Todo classification
        "General tasks and things the user needs to do belong to todo_list.",
        "Examples: wash my car, call John, submit application, attend meeting, pay bill, go to bank, finish project.",
        "If the user says 'add wash my car', use todo_list.",
        "If the user says 'remind me to call John', use todo_list.",
        "If the user says 'add complete my project', use todo_list.",

        # Study classification
        "Study-related subjects and learning activities belong to study_list.",
        "Examples: Python, mathematics, calculus, physics, DBMS, operating systems, machine learning, LangGraph, Agno.",
        "If the user says 'I need to study Python', use study_list.",
        "If the user says 'add DBMS to my study list', use study_list.",
        "If the user says 'add mathematics', use study_list when the context indicates studying mathematics.",

        # Important classification rules
        "Use the meaning and context of the user's request to classify the item.",
        "Words such as buy, purchase, grocery, shopping, food, eat, fruit, vegetable and household shopping usually indicate groceries_list.",
        "Words such as do, finish, complete, call, attend, submit, pay, visit, task and reminder usually indicate todo_list.",
        "Words such as study, learn, revise, exam, chapter, subject, course, practice, notes and programming topics usually indicate study_list.",

        # Operation detection
        "After identifying the list, determine whether the user wants to add, remove, view, or clear items.",
        "For adding an item, delegate to the appropriate agent and use add_items.",
        "For removing an item, delegate to the appropriate agent and use remove_items exactly once.",
        "For viewing one specific list, delegate to the appropriate agent and use list_items.",
        "For viewing all three lists, use the list_all_items Team tool directly.",
        "Only use clear_list when the user explicitly asks to clear the entire list.",

        # All lists
        "If the user says 'list all my lists', 'show all my lists', 'show everything', or 'list everything', use list_all_items.",
        "When showing all lists, show groceries_list, todo_list, and study_list.",

        # Ambiguous requests
        "If the user's request is genuinely ambiguous and there is not enough context to determine the correct list, then ask a clarification question.",
        "Do NOT ask for clarification when the item clearly belongs to one of the three lists.",

        # Exact list names
        "Always use these exact list names:",
        "groceries_list",
        "todo_list",
        "study_list",

        # Delegation
        "The Team Leader should primarily understand, classify, and delegate.",
        "Let the appropriate member agent perform the actual list operation.",
        "Do not unnecessarily perform the same operation multiple times.",

        # Removal rules
        "Never remove an item unless the user explicitly asks to remove it.",
        "When removing an item, call remove_items exactly once with the exact item and exact list name.",
        "Never use clear_list when the user only asks to remove one item.",

        # Examples
        "User: 'Add milk' -> groceries_list -> Grocery Agent -> add milk.",
        "User: 'I need to buy rice' -> groceries_list -> Grocery Agent -> add rice.",
        "User: 'Add mango' -> groceries_list -> Grocery Agent -> add mango.",
        "User: 'Add banana' -> groceries_list -> Grocery Agent -> add banana.",
        "User: 'Add wash my car' -> todo_list -> Todo Agent -> add wash my car.",
        "User: 'Remind me to call Rahul' -> todo_list -> Todo Agent -> add call Rahul.",
        "User: 'I need to study Python' -> study_list -> Study Agent -> add Python.",
        "User: 'Add DBMS to my study list' -> study_list -> Study Agent -> add DBMS.",
        "User: 'Remove milk' -> groceries_list -> Grocery Agent -> remove milk.",
        "User: 'Show my grocery list' -> groceries_list -> Grocery Agent -> list items.",
        "User: 'Show my study list' -> study_list -> Study Agent -> list items.",
        "User: 'List all my lists' -> Team list_all_items tool -> show all three lists.",
        "User: 'Clear my grocery list' -> groceries_list -> Grocery Agent -> clear list."
    ],

    model=llm,
    db=db,
    tools=[list_all_items],
    add_session_state_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    stream=True,
    markdown=True,
    session_state={
        "groceries_list":[],
        "todo_list":[],
        "study_list":[]
    }
)



list_manager.cli_app(stream=True,markdown=True)