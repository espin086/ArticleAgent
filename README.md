# ArticleAgent 📝🤖

ArticleAgent is a Python-based tool designed to automate the creation of Medium articles. It leverages OpenAI's language models to generate engaging and informative content, complete with SEO optimization and markdown formatting. Additionally, it can generate professional images to accompany the articles using DALL-E.

## Features ✨

- **Title Generation**: Automatically generate compelling titles for your articles. 🏷️
- **Outline Creation**: Develop detailed outlines to structure your articles effectively. 🗂️
- **Article Writing**: Compose full-length articles aimed at Engineering and IT decision-makers. 🖋️
- **Image Generation**: Create photo-realistic images to enhance your articles. 🖼️
- **LangChain Tracing**: Track and visualize the execution of your LangChain processes for better debugging and optimization. 🔍

## Installation 🛠️

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/articleagent.git
   cd articleagent
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.11 installed. Then, use Poetry to install the required packages:
   ```bash
   poetry install
   ```

3. **Set Up API Keys**:
   Ensure you have your OpenAI API key set up in your environment. You can do this by exporting it in your terminal:
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   ```

## Usage 🚀

To generate an article and an accompanying image, run the `main.py` script:

```bash
poetry run python main.py
```

This will generate a Medium article on the specified topic and log the article content and image URL.

## Configuration ⚙️

- **Model Selection**: You can specify different models for title, outline, and article generation in the `main.py` script.
- **Logging**: The script uses Python's logging module to provide detailed output of the generation process.
- **LangChain Tracing**: The project uses LangChain's tracing capabilities to monitor and visualize the execution of the LangChain processes. This is useful for debugging and optimizing the workflow.

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact 📧

For questions or feedback, please contact JJ at [4843736+espin086@users.noreply.github.com](mailto:4843736+espin086@users.noreply.github.com).

