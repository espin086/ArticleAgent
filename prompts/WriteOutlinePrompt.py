from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", 
     """
     As an experienced writer, develop a detailed outline for a Medium article on {topic}. 
     The outline should exclude the title and consist of sections labeled with contextually relevant headings that correspond to:

    1.	Introduction: Begin with a section that introduces the topic, capturing the readers attention and setting the stage for the discussion.
	2.	Main Sections: Include 2-3 sections that delve into different facets of the topic, each with a heading that reflects its specific content.
	3.	Conclusion: Conclude with a section that summarizes the key points and provides closure to the article.
	4.	Call to Action: End with a section that encourages readers to take a specific action related to the topic.

    DO:
    - Ensure that each section is labeled with a heading appropriate to its content and the overall theme of the article, avoiding generic labels like Introductionor Conclusion.”

     """
     )
])


if __name__ == "__main__":
    print(prompt_template.invoke({"topic": "cats"}))