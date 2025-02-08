from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper



# Define a concise prompt template
prompt_template = PromptTemplate(
    input_variables=["image_desc"],
    template="""
    Generate an image prompt for: {image_desc}. Make it photo-realistic and professional. Don't use any text in the image.
    """,
)

if __name__ == "__main__":
    print(prompt_template.invoke({"image_desc": "a woman in a professional setting"}))