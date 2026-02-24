from src.tools import tools
from src.tools.web_search import web_search


def test_tools_list_is_not_empty():
    assert len(tools) > 0


def test_web_search_is_in_tools():
    tool_names = [t.name for t in tools]
    assert "web_search" in tool_names


def test_web_search_has_description():
    assert web_search.description
    assert len(web_search.description) > 0
