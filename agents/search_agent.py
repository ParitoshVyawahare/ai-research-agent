import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from utils.web_search import search_web
from utils.vector_store import store_results

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research assistant. 
    Your job is to generate 3 specific search queries for a given topic.
    Return ONLY the queries, one per line, nothing else."""),
    ("human", "Generate 3 search queries for this topic: {topic}")
])

def run_search_agent(topic: str) -> tuple[list[dict], list[str]]:
    print(f"Search Agent thinking about: {topic}")
    
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    
    queries = response.content.strip().split("\n")
    queries = [q.strip() for q in queries if q.strip()]
    print(f"Generated queries: {queries}")
    
    all_results = []
    for query in queries:
        print(f"Searching: {query}")
        results = search_web(query, max_results=3)
        all_results.extend(results)
    
    store_results(all_results)
    print(f"Search Agent done! Found {len(all_results)} total results")
    
    return all_results, queries