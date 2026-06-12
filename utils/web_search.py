import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Takes a search query, returns list of results
    Each result has: title, url, content
    """
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )

    results = []
    for r in response["results"]:
        results.append({
            "title": r["title"],
            "url": r["url"],
            "content": r["content"]
        })

    return results


def format_results(results: list[dict]) -> str:
    """
    Converts results list into clean readable text
    for passing into the LLM
    """
    formatted = ""
    for i, r in enumerate(results, 1):
        formatted += f"""
Result {i}:
Title: {r['title']}
URL: {r['url']}
Content: {r['content']}
---
"""
    return formatted