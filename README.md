# ArticleAgent

**Automated Medium article generation powered by OpenAI and LangChain**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-orange.svg)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o%20%7C%20o3--mini%20%7C%20DALL--E%203-412991.svg)](https://openai.com/)

ArticleAgent is a Python-based automation tool that generates publication-ready Medium articles with accompanying professional images. It orchestrates multiple AI models through LangChain to handle title creation, outlining, writing, editing, and image generation — all from a single topic input.

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                         CLI (argparse)                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ topic
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                            │
│              main.py — generate_article_process()                   │
│                                                            ┌──────┐│
│              Traced via @traceable decorator ──────────────►│Trace ││
│                                                            └──────┘│
└───┬──────────┬──────────┬──────────┬──────────┬─────────────────────┘
    │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌──────────┐
│ Write  ││ Write  ││ Write  ││ Edit   ││ Generate │  PROMPT
│ Title  ││Outline ││Article ││Article ││  Image   │  TEMPLATES
│ Prompt ││ Prompt ││ Prompt ││ Prompt ││  Prompt  │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘└────┬─────┘
    │         │         │         │           │
    ▼         ▼         ▼         ▼           ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌──────────┐
│gpt-4o  ││o3-mini ││o3-mini ││o3-mini ││ DALL-E 3 │  OPENAI
│ -mini  ││        ││        ││        ││          │  MODELS
└────────┘└────────┘└────────┘└────────┘└──────────┘

                    ┌──────────────────┐
                    │    MONITORING    │
                    │LangSmith Tracing │
                    └──────────────────┘
```

### Article Generation Pipeline

The pipeline follows a multi-stage process with parallel execution where possible:

```
                                          ┌─────────────────────┐
                                     ┌───►│ 2a. Generate Outline │
                                     │    │      (o3-mini)       │──┐
┌─────────┐   ┌──────────────────┐   │    └─────────────────────┘  │  ┌──────────────────┐
│  Topic   │──►│ 1. Generate Title│───┤                             ├─►│ 3. Write Article │
│  Input   │   │   (gpt-4o-mini)  │   │   PARALLEL                 │  │    (o3-mini)     │
└─────────┘   └──────────────────┘   │   (asyncio.gather)          │  └────────┬─────────┘
                                     │    ┌─────────────────────┐  │           │
                                     └───►│ 2b. Generate Image  │  │           ▼
                                          │    (DALL-E 3)       │──┘  ┌──────────────────┐
                                          └─────────┬───────────┘     │ 4. Edit & Review │
                                                    │                 │    (o3-mini)     │
                                                    ▼                 └────────┬─────────┘
                                              ┌───────────┐                    │
                                              │ Image URL │                    ▼
                                              └─────┬─────┘           ┌───────────────┐
                                                    │                 │ Final Article │
                                                    │                 └───────┬───────┘
                                                    ▼                         ▼
                                              ┌──────────────────────────────────┐
                                              │            OUTPUT                │
                                              │   (final_article, image_url)     │
                                              └──────────────────────────────────┘
```

### Data Flow

```
User            main.py          OpenAI API
 │                │                   │
 │── topic ──────►│                   │
 │                │                   │
 │                │── generate_title ─────────────────►│
 │                │   (gpt-4o-mini, temp=0)            │
 │                │◄── title ──────────────────────────│
 │                │                                    │
 │                │       ┌── PARALLEL ──────────┐     │
 │                │       │                      │     │
 │                │── generate_outline ──────────────►│
 │                │       │  (o3-mini)           │     │
 │                │◄── outline ─────────────────────── │
 │                │       │                      │     │
 │                │── generate_article_image ────────►│
 │                │       │  (DALL-E 3, HD)      │     │
 │                │◄── image_url ───────────────────── │
 │                │       │                      │     │
 │                │       └──────────────────────┘     │
 │                │                                    │
 │                │── generate_article ───────────────►│
 │                │   (o3-mini, title + outline)       │
 │                │◄── article_draft ──────────────────│
 │                │                                    │
 │                │── edit_evaluate_article ──────────►│
 │                │   (o3-mini)                        │
 │                │◄── final_article ──────────────────│
 │                │                                    │
 │◄── (article, ──│                                    │
 │    image_url)  │                                    │
```

### Model Usage by Stage

```
┌──────────────────┐     ┌────────────────────────────────────┐
│     STAGE 1      │     │        STAGE 2 (PARALLEL)          │
│                  │     │                                    │
│  Title           │     │  Outline          Image            │
│  Generation      │     │  Creation         Generation       │
│       │          │     │       │                │           │
│       ▼          │     │       ▼                ▼           │
│  ┌──────────┐   │     │  ┌─────────┐     ┌──────────┐     │
│  │gpt-4o-   │   │────►│  │ o3-mini │     │ DALL-E 3 │     │
│  │mini      │   │     │  │         │     │1024x1024 │     │
│  │temp=0    │   │     │  └─────────┘     │   HD     │     │
│  └──────────┘   │     │                  └──────────┘     │
└──────────────────┘     └───────────────────┬───────────────┘
                                             │
                                             ▼
┌──────────────────┐     ┌──────────────────────────────────┐
│     STAGE 3      │     │           STAGE 4                │
│                  │     │                                  │
│  Article         │     │  Edit & Review                   │
│  Writing         │     │                                  │
│       │          │     │       │                          │
│       ▼          │     │       ▼                          │
│  ┌─────────┐    │     │  ┌─────────┐                    │
│  │ o3-mini │    │────►│  │ o3-mini │                    │
│  │         │    │     │  │         │                    │
│  └─────────┘    │     │  └─────────┘                    │
└──────────────────┘     └──────────────────────────────────┘
```

---

## Features

- **Title Generation** -- Creates compelling, SEO-optimized titles (60 characters max) using GPT-4o-mini
- **Outline Creation** -- Develops structured outlines with introduction, main sections, conclusion, and call-to-action
- **Article Writing** -- Generates ~1,000-word markdown articles targeted at Engineering and IT decision-makers
- **Image Generation** -- Produces professional photo-realistic images via DALL-E 3 (1024x1024, HD quality)
- **Article Review & Editing** -- Automatic review for coherence, brevity, organization, and factual accuracy
- **Async Processing** -- Concurrent execution of outline and image generation via `asyncio.gather`
- **LangSmith Tracing** -- Full execution tracking and visualization for debugging and optimization

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| LLM Orchestration | LangChain 0.3 | Prompt chaining and LLM pipeline management |
| LLM Provider | OpenAI API | GPT-4o-mini, o3-mini, DALL-E 3 |
| Monitoring | LangSmith | Execution tracing, performance monitoring |
| Async Runtime | asyncio | Concurrent task execution |
| CLI | argparse | Command-line interface |
| Package Management | Poetry | Dependency management and virtual environments |

---

## Project Structure

```
ArticleAgent/
├── main.py                         # Entry point and pipeline orchestration
├── config.py                       # Configuration constants (LangSmith project name)
├── prompts/                        # LangChain prompt templates
│   ├── __init__.py
│   ├── WriteTitlePrompt.py         # Title generation prompt
│   ├── WriteOutlinePrompt.py       # Outline generation prompt
│   ├── WriteArticlePrompt.py       # Article writing prompt
│   ├── GenerateImagePrompt.py      # DALL-E image prompt
│   └── EditArticlePrompt.py        # Article review/editing prompt
├── pyproject.toml                  # Poetry dependencies and project metadata
├── poetry.lock                     # Locked dependency versions
├── LICENSE                         # MIT License
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) package manager
- OpenAI API key

### Setup

```bash
# Clone the repository
git clone https://github.com/espin086/ArticleAgent.git
cd ArticleAgent

# Install dependencies
poetry install

# Set required environment variables
export OPENAI_API_KEY='your-openai-api-key'

# Optional: Enable LangSmith tracing
export LANGSMITH_API_KEY='your-langsmith-api-key'
```

---

## Usage

Generate an article on any topic with a single command:

```bash
poetry run python main.py --topic "Your Topic Here"
```

### Example

```bash
poetry run python main.py --topic "The Future of Edge Computing in Enterprise Architecture"
```

This will:

1. Generate an SEO-optimized title
2. Create a structured outline and professional image in parallel
3. Write a ~1,000-word markdown article
4. Review and polish the article for publication quality
5. Output the final article text and image URL

---

## How It Works

### Pipeline Stages

| Stage | Function | Model | Description |
|-------|----------|-------|-------------|
| 1 | `generate_title()` | gpt-4o-mini (temp=0) | Creates a deterministic, SEO-optimized title |
| 2a | `generate_outline()` | o3-mini | Builds structured outline with sections and CTA |
| 2b | `generate_article_image()` | DALL-E 3 | Generates a photo-realistic companion image |
| 3 | `generate_article()` | o3-mini | Writes the full article from title + outline |
| 4 | `edit_evaluate_article()` | o3-mini | Reviews for coherence, brevity, accuracy |

Stages 2a and 2b run concurrently using `asyncio.gather()` for reduced latency.

### Prompt Engineering

Each stage uses a dedicated prompt template in the `prompts/` directory. Prompts are built with LangChain's `ChatPromptTemplate` and piped directly into the model using the `|` operator:

```python
chain = prompt | ChatOpenAI(model="o3-mini")
response = await chain.ainvoke({"topic": title})
```

### Monitoring

The main orchestration function is decorated with `@traceable` for LangSmith integration, providing visibility into token usage, latency, and execution flow across the entire pipeline.

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API authentication key |
| `LANGSMITH_API_KEY` | No | Enables LangSmith tracing and monitoring |

Model selection and parameters can be adjusted directly in `main.py` function signatures.

---

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request for any improvements or bug fixes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
