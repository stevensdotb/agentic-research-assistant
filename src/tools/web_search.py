from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search from the internet update technical information.
    Use it when the user asks for something that doesn't know or is a recent event.
    """
    try:
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(query)
    except Exception as e:
        return f"Error searching: {e}. Please, try to reason about your previous knowledge and suggest another query"
