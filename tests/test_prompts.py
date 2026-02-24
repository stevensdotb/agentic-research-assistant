from src.prompts import RESEARCHER_SYSTEM_PROMPT, FINAL_SYNTHESIS_PROMPT, EVALUATOR_PROMPT


def test_researcher_prompt_has_date_placeholder():
    assert "{current_date}" in RESEARCHER_SYSTEM_PROMPT
    formatted = RESEARCHER_SYSTEM_PROMPT.format(current_date="2026-01-01")
    assert "2026-01-01" in formatted


def test_evaluator_prompt_has_placeholders():
    assert "{user_question}" in EVALUATOR_PROMPT
    assert "{current_response}" in EVALUATOR_PROMPT
    formatted = EVALUATOR_PROMPT.format(
        user_question="What is AI?",
        current_response="AI is artificial intelligence.",
    )
    assert "What is AI?" in formatted
    assert "AI is artificial intelligence." in formatted


def test_final_synthesis_prompt_is_static():
    # No placeholders — should not raise on .format()
    assert "{" not in FINAL_SYNTHESIS_PROMPT.replace("{{", "").replace("}}", "")
