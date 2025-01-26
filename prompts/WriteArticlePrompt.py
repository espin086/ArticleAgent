from langchain_core.prompts import PromptTemplate

WriteArticlePrompt = PromptTemplate.from_template(
    """
    You are a writer for a tech blog. You are given a topic and you need to write an article about it.
    Here is the topic: {topic}
    """
)

if __name__ == "__main__":
    print(WriteArticlePrompt.invoke({"topic":"The future of AI in healthcare"}))