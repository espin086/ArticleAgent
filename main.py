"""
This script generates a medium article about a given topic.
"""
import openai 
from prompts.WriteArticlePrompt import prompt_template
from langchain_openai import ChatOpenAI
from langsmith import wrappers, traceable



# auto-trace LLM calls in-context
client = wrappers.wrap_openai(openai.Client())

@traceable
def generate_article(topic:str, model:str="gpt-3.5-turbo", temperature:float=0) -> str:
    """
    Generate an medium article about a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = prompt_template | llm
    return chain.invoke({"topic":topic})



if __name__ == "__main__":
    print(generate_article("The future of AI in healthcare"))



