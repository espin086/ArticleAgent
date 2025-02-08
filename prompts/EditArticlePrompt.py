from langchain_core.prompts import ChatPromptTemplate

edit_evaluate_prompt_template = ChatPromptTemplate([
    ("system", "You are an expert article editor and evaluator."),
    ("user", """
    Please edit and evaluate the following article. Focus on the following aspects:
    
    1. Coherence: Ensure the article flows logically and ideas are connected.
    2. Brevity: Make the article concise without losing essential information.
    3. Remove Wordiness: Eliminate unnecessary words and phrases.
    4. Organization: Improve the structure for better readability.

    Article:
    {article}
    """)
])