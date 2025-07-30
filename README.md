# Perplexity CLI

A command-line interface that replicates the core functionality of Perplexity. It takes a user's query, fetches live search results from the web, and uses an AI model to synthesize a cited answer from the results.

## Features

- **Web Search Integration**: Uses SerpAPI to fetch real-time search results from Google.
- **AI-Powered Synthesis**: Leverages OpenAI's GPT models to generate a comprehensive answer based on the search results.
- **Streaming Responses**: The AI's answer is streamed to the terminal word-by-word for an interactive experience.
- **Inline Citations**: The generated answer includes numbered citations `[1]` that link back to the original sources.
- **Follow-up Questions**: After providing an answer, the AI suggests relevant follow-up questions for deeper exploration.
- **Rich Terminal UI**: Built with the `rich` library for a clean, modern interface with formatted tables, progress spinners, and color-coded text.
- **Interactive & Single-Query Modes**: Can be run as an interactive session or with a single query from the command line.
- **Simple Caching**: Caches search results to improve performance and reduce API costs for repeated queries.
- **Configurable Model**: Allows the user to specify which OpenAI model to use (e.g., `gpt-4o-mini`, `gpt-4o`).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd perplexity-cli
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API keys:**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Edit the new `.env` file and add your API keys for SerpAPI and OpenAI.

## Usage

### Interactive Mode

To start an interactive session, simply run:
```bash
python cli.py
```
You can then type your queries at the prompt. Type `exit` or `quit` to end the session.

### Command-Line Mode

To get a single answer directly, use the `--query` or `-q` flag:
```bash
python cli.py -q "What is quantum computing?"
```

### Options

-   `-q`, `--query`: The search query. If not provided, the tool runs in interactive mode.
-   `-r`, `--results`: The number of search results to fetch (default: 5).
-   `-m`, `--model`: The OpenAI model to use (default: `gpt-4o-mini`).
-   `--no-cache`: Disables using the cache for the current query.
-   `--clear-cache`: Clears all cached data.

### Examples

#### Basic Usage
```bash
# Simple query with default settings
python cli.py -q "what is quantum computing"

# Interactive mode - multiple queries in one session
python cli.py
# Then type your queries, use 'exit' to quit
```

#### Test AI-Powered Features

**1. Query Optimization (Automatic Temporal Context)**
```bash
# These queries automatically get optimized with current date/time
python cli.py -q "latest news" --no-cache
python cli.py -q "current events" --no-cache
python cli.py -q "trending topics today" --no-cache
```

**2. Source Quality Scoring (Look for ⭐ markers)**
```bash
# Prioritizes authoritative sources (.gov, .edu, major news)
python cli.py -q "climate change research"
python cli.py -q "NASA space missions"
python cli.py -q "COVID-19 vaccine information"
```

**3. Follow-up Question Generation**
```bash
# Complex queries that generate intelligent follow-ups
python cli.py -q "explain quantum computing"
python cli.py -q "how does photosynthesis work"
python cli.py -q "what is blockchain technology"
```

#### Advanced Options

**Different AI Models**
```bash
# Default fast model
python cli.py -q "explain neural networks"

# More powerful model for complex queries
python cli.py -q "compare RISC vs CISC architectures" -m gpt-4o -r 10
```

**Control Search Results**
```bash
# Fewer results for quick answers
python cli.py -q "Python vs JavaScript" -r 3

# More results for comprehensive research
python cli.py -q "machine learning algorithms" -r 10
```

**Caching Controls**
```bash
# First run - fetches fresh results
python cli.py -q "test query"

# Second run - uses cache (notice "Using cached results" message)
python cli.py -q "test query"

# Force fresh results
python cli.py -q "breaking news today" --no-cache

# Clear all cached data
python cli.py --clear-cache
```

#### Real-World Test Queries

**Company Research**
```bash
python cli.py -q "What is OpenAI and what do they do?"
python cli.py -q "Tell me about Anthropic AI company"
```

**Technical Questions**
```bash
python cli.py -q "How to implement binary search in Python"
python cli.py -q "Explain REST API best practices"
python cli.py -q "What are microservices architecture patterns"
```

**Current Events (with --no-cache for freshness)**
```bash
python cli.py -q "What happened in tech news today" --no-cache
python cli.py -q "Latest AI breakthroughs 2024" --no-cache
```

**Comparison Queries (Tests Query Optimization)**
```bash
python cli.py -q "React vs Vue vs Angular"
python cli.py -q "AWS vs Google Cloud vs Azure comparison"
```

#### Run the Demo
```bash
# See all features in action with a guided demo
python demo.py
```

#### Run Tests
```bash
# Run the test suite
python run_tests.py
```
