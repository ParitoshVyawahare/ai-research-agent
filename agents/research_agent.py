import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from utils.vector_store import retrieve_relevant

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert research analyst.
    You will be given content from multiple articles about a topic.
    Your job is to extract and summarize the most important insights.
    Focus on: key findings, important facts, recent developments.
    Be concise but thorough."""),
    ("human", """Topic: {topic}
    
Here is the research content:
{context}

Extract the most important insights from this content.""")
])

def run_research_agent(topic: str) -> tuple[str, list[dict]]:
    print(f"Research Agent analyzing: {topic}")

    relevant_docs = retrieve_relevant(topic, n_results=5)
    
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"""
Source {i}: {doc['title']}
URL: {doc['url']}
Content: {doc['content']}
---
"""

    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "context": context
    })

    print("Research Agent done!")
    return response.content, relevant_docs