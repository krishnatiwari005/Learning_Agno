from agno.agent import Agent
from agno.models.groq import Groq
from agno.workflow import Workflow,Step,Loop,StepOutput
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

def word_count_condition(step_output:list[StepOutput])->bool:
    "Condition to check if the story is less than 150 words"
    if step_output:
        for output in step_output:
            story_content:str =output.content
            word_count:int =len(story_content.split(" "))
            if word_count<=150:
                return True
            else:
                return False
    else:
        return False

story_generation_agent=Agent(
    id="story-generation-agent",
    name="Story Generation Agent",
    instructions=["you are an expert story writer",
                  "create interested ,engaging and imaginative story in based on user's input",
                  "stick to the wordlimit requested by user"],
    model=llm
)

story_generation_step=Step(
    name="story generation step",
    agent=story_generation_agent,
    description="generate a short story based on user's prompt"
)

looping_step=Loop(
    steps=[story_generation_step],
    name="Story generation loop",
    description="generates story in loop untill the given condition are met",
    end_condition=word_count_condition,
)

worflow=Workflow(
    id="story-generation-workflow",
    name="Story Generation Workflow",
    steps=[looping_step],
    description="A workflow that generates a short stories while ensuring the length of story should not exceeds the max-limit using looping mechanism"
)

worflow.print_response(input="title: a little girl!! in 100 words",stream=True,markdown=True)