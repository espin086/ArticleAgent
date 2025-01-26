
from langchain_openai import ChatOpenAI
from prompts.WriteArticlePrompt import WriteArticlePrompt




print(WriteArticlePrompt.invoke({"topic":"The future of AI in healthcare"}))