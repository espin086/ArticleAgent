from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Write a medium article about {topic}")
])


if __name__ == "__main__":
    print(prompt_template.invoke({"topic": "cats"}))