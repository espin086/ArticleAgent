from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", """
     
    As an experienced writer, compose a 1,000-word Medium article on {topic} aimed at Engineering and IT decision makers. 
    The article should be informative and engaging, written in a conversational tone. 
    
     Structure the content as follows:

     {outline}


     SEO Optimization: The article should be SEO optimized and include relevant keywords.
     Formatting: The article should be formatted in markdown.
     No Placeholders: Do not use placeholders like {topic} or {outline} in the article.
     No links: Do not include links in the article.
     """)
])


if __name__ == "__main__":
    print(prompt_template.invoke({"topic": "cats", "outline": "introduction, main content, conclusion, summary" }))