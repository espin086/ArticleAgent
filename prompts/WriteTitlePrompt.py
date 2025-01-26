from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", """
     As an experienced editor, craft a compelling Medium article title for the topic {topic}.
     
     Style: The title should be engaging, informative, and no longer than 60 characters. 
     
     Content: Incorporate relevant keywords and use persuasive language to highlight the unique aspects of the topic, 
     ensuring it attracts and resonates with the intended readers.

     Audience: The target audience IT and Engineering decision makers looking for insights and trends in the industry.
     """),
])


if __name__ == "__main__":
    print(prompt_template.invoke({"topic": "cats"}))