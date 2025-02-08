"""
This script generates a medium article about a given topic.
"""
import logging
import openai 
import argparse
import asyncio

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

async def generate_title(topic: str, model: str = "gpt-4o-mini", temperature: float = 0) -> str:
    """
    Generate a medium article title for a given topic.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    chain = write_title_prompt_template | llm
    return chain.invoke({"topic": topic})

async def generate_outline(topic: str, model: str = "o3-mini") -> str:
    """
    Generate an outline for a medium article about a given topic.
    """
    llm = ChatOpenAI(model=model)
    chain = write_outline_prompt_template | llm
    return chain.invoke({"topic": topic})

async def generate_article(topic: str, outline: str, model: str = "o3-mini") -> str:
    """
    Generate a medium article about a given topic.
    """
    llm = ChatOpenAI(model=model)
    chain = write_article_prompt_template | llm
    return chain.invoke({"topic": topic, "outline": outline})

async def generate_article_image(topic: str) -> str:
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

async def edit_evaluate_article(article: str, model: str = "o3-mini") -> str:
    """
    Edit and evaluate the article for coherence, brevity, wordiness, accuracy,and organization.
    """
    llm = ChatOpenAI(model=model)
    chain = edit_evaluate_prompt_template | llm
    return chain.invoke({"article": article})

@traceable(project_name=LANGSMITH_PROJECT_NAME)
async def generate_article_process(topic: str) -> str:
    """
    Orchestrates the generation of a medium article by first generating a title,
    then an outline, and finally the article itself.
    """
    logger.info("Generating title...")
    title = await generate_title(topic)
    logger.info("Generating outline and image concurrently...")
    outline_task = asyncio.create_task(generate_outline(topic=title))
    image_task = asyncio.create_task(generate_article_image(topic=title))

    outline, image_url = await asyncio.gather(outline_task, image_task)

    logger.info("Generating article...")
    article_draft = await generate_article(topic=title, outline=outline)

    logger.info("Editing and evaluating article...")
    article = await edit_evaluate_article(article_draft)
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
    article, image_url = asyncio.run(generate_article_process(topic))
    logger.info("Article generated: %s", article)
    logger.info("Image URL: %s", image_url)

