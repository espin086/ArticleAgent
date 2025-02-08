from langchain_core.prompts import ChatPromptTemplate

edit_evaluate_prompt_template = ChatPromptTemplate([
    ("system", "You are an expert article editor and evaluator."),
    ("user", """
    Please edit the following article. Focus on the following aspects:
    
    1. Coherence: Ensure the article flows logically and ideas are connected.
    2. Brevity: Make the article concise without losing essential information.
    3. Remove Wordiness: Eliminate unnecessary words and phrases.
    4. Organization: Improve the structure for better readability.
    5. Fact Check: Ensure the article is factually accurate and doesn't contain any errors.

    Article:
    {article}
    """)
])