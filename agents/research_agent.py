import sys
import os
from tavily import TavilyClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def research_agent(query, num_results=5):
    try:
        results = tavily.search(query=query, num_results=num_results)
        
        if not isinstance(results, list):
            return None
        
        return [
            {
                "title": item.get("title", "No Title"),
                "snippet": item.get("snippet", "No Snippet"),
                "url": item.get("url", "No URL")
            }
            for item in results
        ]
    except:
        return None

if __name__ == "__main__":
    test_query = "AI in Healthcare"
    search_results = research_agent(test_query)
    
    if search_results:
        print(search_results)
    else:
        print("No valid results found.")
