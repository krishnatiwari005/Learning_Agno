from agno.agent import Agent
from agno.models.groq import Groq
from agno.workflow import Workflow,Step,Loop,StepOutput,Condition,StepInput
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

def email_review_condition(step_input:StepInput)->bool:
    """condition to check if the email has the subject line""" 
    email_content=step_input.previous_step_content or ""
    if email_content:
        email_content=email_content.lower()

        if "subject" in email_content:
            return True
        else:
            return False
    else:
        return False

def email_output(step_input:StepInput)->StepOutput:
    "return the output of the drafting step"
    email_content=step_input.get_step_content("Email draft step")
    return StepOutput(step_name="Email output step",content=f"{email_content}",executor_type="function")

email_draft_agent=Agent(
    id="email-draft-agent",
    name="Email Draft agent",
    instructions=["you are an expert in drafting email",
                  "draft clear and professional email based on user's input",
                  "output in a proper format"],
    model=llm,
    markdown=True
)

email_draft_step=Step(
    name="Email draft step",
    agent=email_draft_agent,
    description="draft and email based on user's input prompt"
)

email_output_step=Step(
    name="Email output step",
    executor=email_output,
    description="output my email to the end user"
)

review_email_step=Condition(
    evaluator=email_review_condition,
    steps=[email_output_step],
    name="Review Email Step",
    description="revise the drafted email if it contains the subject line"
)

workflow=Workflow(
    id="email-workflow",
    name="Email Drafting and review workflow",
    steps=[email_draft_step,review_email_step],
    description="A waskflow that draft an email based on user reviews it if the subject is present or not "
)

workflow.print_response(input="Draft an email to schedule meeting with my technical team at 6 pm the email should be in a proper format without a subject line ")
