import sys
import os
import google.generativeai as genai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def answer_drafter(research_data):
    if not research_data:
        return "No data provided"
    
    formatted_data = "\n\n".join(
        ["Title: " + item.get("title", "No Title") + "\nSnippet: " + item.get("snippet", "No Snippet") + "\nURL: " + item.get("url", "No URL") for item in research_data]
    )
    
    prompt = "Summarize this research:\n" + formatted_data
    
    try:
        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text
        return "Couldn't generate summary"
    except:
        return "Error while processing"
