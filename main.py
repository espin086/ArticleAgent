"""
This script generates a medium article about a given topic.
"""
import openai 
from prompts.WriteArticlePrompt import prompt_template as write_article_prompt_template
from langchain_openai import ChatOpenAI
from langsmith import wrappers, traceable
from config import LANGSMITH_PROJECT_NAME


# auto-trace LLM calls in-context
client = wrappers.wrap_openai(openai.Client())

@traceable(project_name=LANGSMITH_PROJECT_NAME)
def generate_article(topic:str, model:str="gpt-3.5-turbo", temperature:float=0) -> str:
    """
    Generate an medium article about a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = write_article_prompt_template | llm
    return chain.invoke({"topic":topic})



if __name__ == "__main__":
    print(generate_article("The future of AI in healthcare"))



