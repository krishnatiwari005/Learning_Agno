import os
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.run import RunContext
from textwrap import dedent
load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

db=SqliteDb(db_file="chat_history.db")

def add_key_point(run_context:RunContext,point:str)->str:
    """tool to add key points to the session state"""
    points_list=run_context.session_state['key_points']
    points_list.append(point)
    return f"point: {point} added to the session state"

agent=Agent(
    name="my-agent",
    model=llm,
    markdown=True,
    stream=True,
    db=db,
    tools=[add_key_point],
    session_state={"key_points":[]},
    add_history_to_context=True,
    instructions=dedent("""
                          you are the expert assistant your task is to:
                          1:create summary of the topic and stick to the word count if provided,
                          2:you have access to the tool called as add_key_points, which add key points from summary to the session state,
                          3:add key points only when asked for,
                          4:summary created should have both advantage and disadvantage.
                        """),
    num_history_runs=5,
    session_id="session-2",
    user_id="user1",
    add_session_state_to_context=True
)

agent.print_response(input="write a summary in 100 words on topic: Current ai evolution in india")
agent.print_response("add all the key points from the summary ,number of keypoints depend on summary's strength")
agent.print_response(input="what are we talking about right now?")
print(agent.get_session_state("session-2"))