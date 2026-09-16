from agno.models.groq import Groq
from agno.agent import Agent
from agno.workflow import Step,Workflow
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

essay_writing_agent=Agent(
    name="Eassay writing agent",
    id="essay_writing",
    model=llm,
    instructions=["you are an expert in writing essay",
                  "write well structured essay on the variety of topic",
                  "Limit your response to maximum of 350 words"]
)

extraction_agent=Agent(
    id="extraction_agent",
    name="Extraction agent",
    instructions=["you are an expert in extracting the importing points from the generated essay",
                  "summarize the key points in a concise manner",
                  "your are output should be in a good structured"],
    model=llm
)

essay_writing_step=Step(
    name="Essay writing step",
    agent=essay_writing_agent,
    description="Generates an essay based on the user topic",
)

extraction_step=Step(
    name="information extraction agent",
    agent=extraction_agent,
    description="Extract important point from the essay generated in the previous step"
)

workflow=Workflow(
    id="work_flow_agent",
    name="Essay writing and point extraction workflow",
    steps=[essay_writing_step,extraction_step],
    description=["workflow that first write an essay on a given topic and then extract important points from that essay"]
)

workflow.print_response(input="topic: impact of ai on education",stream=True,markdown=True)
