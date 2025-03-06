import sys
import os
import langgraph.graph as lg
from tavily import TavilyClient
import google.generativeai as genai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import TAVILY_API_KEY, GEMINI_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def research_agent(data):
    query = data.get("query", "").strip()
    num_results = data.get("num_results", 3)

    if not query:
        return None
    
    try:
        results = tavily.search(query=query, num_results=num_results)

        if not results or "results" not in results or not isinstance(results["results"], list):
            return None

        search_results = [
            {
                "title": item.get("title", "No Title"),
                "snippet": item.get("content", "No Snippet"),
                "url": item.get("url", "No URL")
            }
            for item in results["results"]
        ]

        return {"search_results": search_results} if search_results else None
    except Exception:
        return None

def answer_drafter(data):
    if not data or "search_results" not in data:
        return None

    search_results = data["search_results"]
    formatted_data = "\n\n".join(
        [f"Title: {item['title']}\nSnippet: {item['snippet']}\nURL: {item['url']}" for item in search_results]
    )

    prompt = f"Summarize the following research findings:\n\n{formatted_data}"

    try:
        response = model.generate_content(prompt)
        return {"summary": response.text} if response and response.text else None
    except Exception:
        return None

workflow = lg.Graph()
workflow.add_node("research", research_agent)
workflow.add_node("answer_drafter", answer_drafter)
workflow.set_entry_point("research")
workflow.add_edge("research", "answer_drafter")
workflow.set_finish_point("answer_drafter")

research_workflow = workflow.compile()
