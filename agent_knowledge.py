from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.knowledge import Knowledge
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY","").strip()
hf_api_key=os.getenv("HUGGINGFACE_API_KEY","").strip()

llm=Groq(id="openai/gpt-oss-20b",api_key=api_key)

embedder=HuggingfaceCustomEmbedder(api_key=hf_api_key)

chunking_strategy=SemanticChunking(embedder=embedder,chunk_size=1000)

reader=PDFReader(chunking_strategy=chunking_strategy)

vector_db=LanceDb(uri="vector_db/lancedb",table_name="knowledge_base",embedder=embedder)

knowledge_base=Knowledge(name="Knowledge_base",description="contains the notes on : constition of india",vector_db=vector_db)

if __name__=="__main__": 
   knowledge_base.insert(path="text.pdf",reader=reader)

