"""
This script generates a medium article about a given topic.
"""
import logging
import openai 
import argparse


from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langsmith import wrappers, traceable
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from prompts.WriteTitlePrompt import prompt_template as write_title_prompt_template
from prompts.WriteOutlinePrompt import prompt_template as write_outline_prompt_template
from prompts.WriteArticlePrompt import prompt_template as write_article_prompt_template
from prompts.GenerateImagePrompt import prompt_template as generate_image_prompt_template
from prompts.EditArticlePrompt import edit_evaluate_prompt_template


from config import LANGSMITH_PROJECT_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# auto-trace LLM calls in-context
client = wrappers.wrap_openai(openai.Client())


def generate_title(topic:str, model:str="gpt-4o-mini", temperature:float=0) -> str:
    """
    Generate an medium article title for a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = write_title_prompt_template | llm
    return chain.invoke({"topic":topic})

def generate_outline(topic:str, model:str="gpt-4o-mini", temperature:float=0) -> str:
    """
    Generate an outline for a medium article about a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = write_outline_prompt_template | llm
    return chain.invoke({"topic":topic})


def generate_article(topic:str, outline:str, model:str="gpt-4o-mini", temperature:float=0) -> str:
    """
    Generate an medium article about a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = write_article_prompt_template | llm
    return chain.invoke({"topic":topic, "outline":outline})


def generate_article_image(topic:str) -> str:
    """
    Generate an image for a medium article about a given topic.
    """
    prompt = generate_image_prompt_template.invoke({"image_desc": topic})
    prompt = prompt.to_string()
    logger.info("Prompt: %s", prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        response_format="url",
    )
    return response.data[0].url


def edit_evaluate_article(article: str, model: str = "gpt-4o-mini", temperature: float = 0) -> str:
    """
    Edit and evaluate the article for coherence, brevity, wordiness, and organization.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = edit_evaluate_prompt_template | llm
    return chain.invoke({"article": article})

@traceable(project_name=LANGSMITH_PROJECT_NAME)
def generate_article_process(topic: str) -> str:
    """
    Orchestrates the generation of a medium article by first generating a title,
    then an outline, and finally the article itself.
    """
    logger.info("Generating title...")
    title = generate_title(topic)
    
    logger.info("Generating outline...")
    outline = generate_outline(topic=title)
    
    logger.info("Generating article...")
    article_draft = generate_article(topic=title, outline=outline)
    
    logger.info("Editing and evaluating article...")
    article = edit_evaluate_article(article_draft)
    
    logger.info("Generating image...")
    image_url = generate_article_image(topic=title)
    
    return article, image_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Medium article and an accompanying image based on a given topic."
    )
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="The topic for which to generate the Medium article and image."
    )
    args = parser.parse_args()

    topic = args.topic
    article, image_url = generate_article_process(topic)
    logger.info("Article generated: %s", article)
    logger.info("Image URL: %s", image_url)

