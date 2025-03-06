import sys
import os
from workflows.research_workflow import research_workflow
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if __name__ == "__main__":
    print("\nWelcome to the Deep Research AI System!\n")
    
    query = input("Enter your research topic: ").strip()
    
    if not query:
        print("\nError: Query cannot be empty.")
        sys.exit(1)
    
    print("\nProcessing your research request...\n")
    
    result = research_workflow.invoke({"query": query, "num_results": 3})

    if not result:
        print("\nError: No results found.")
    elif isinstance(result, dict) and "error" in result:
        print("\nError:", result["error"])
    else:
        print("\nFinal Research Summary:\n\n", result.get("summary", "No summary available."))
