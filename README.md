# Perplexity CLI

A command-line interface clone of Perplexity that combines web search results with AI-powered responses and citations.

## Features

- **Web Search Integration**: Uses SerpAPI to fetch real-time search results from Google
- **AI-Powered Responses**: Leverages OpenAI's GPT models to synthesize search results into comprehensive answers
- **Streaming Responses**: Watch AI responses generate in real-time with live updates
- **Inline Citations**: AI responses include numbered citations that link back to source materials
- **Interactive & Command-Line Modes**: Use interactively or pass queries directly via command line
- **Rich Terminal UI**: Beautiful formatting with colored output, tables, and progress indicators
- **Smart Caching**: Reduces API costs with intelligent caching of search results and AI responses
- **Follow-up Questions**: AI suggests relevant follow-up questions based on your query
- **Multiple Models**: Support for different OpenAI models (gpt-4o-mini, gpt-4o, etc.)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd perplexity-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `SERPAPI_KEY`: Get from https://serpapi.com/
- `OPENAI_API_KEY`: Get from https://platform.openai.com/

## Usage

### Interactive Mode
```bash
python cli.py
```

### Command-Line Mode
```bash
python cli.py -q "What is quantum computing?"
```

### Options
- `-q, --query`: Search query (if not provided, interactive mode is used)
- `-r, --results`: Number of search results to fetch (default: 5)
- `-m, --model`: OpenAI model to use (default: gpt-4o-mini)
- `--no-cache`: Disable caching for this query
- `--clear-cache`: Clear all cached data

## How It Works

1. **Search Phase**: Queries are sent to SerpAPI which returns Google search results including titles, snippets, and URLs
2. **AI Processing**: Search results are passed to GPT-4o-mini with instructions to synthesize a comprehensive answer
3. **Citation Extraction**: The AI includes inline citations [1], [2], etc. which are parsed and linked to sources
4. **Display**: Results are formatted using Rich library for an enhanced terminal experience

## Technical Choices

- **Python**: Chosen for rapid development and excellent library ecosystem
- **Click**: Provides clean CLI interface with minimal boilerplate
- **Rich**: Creates beautiful terminal output with tables, colors, and formatting
- **SerpAPI**: Reliable search API with good documentation and free tier
- **OpenAI GPT-4o-mini**: Fast, cost-effective model that handles synthesis well
- **Citation System**: Regex-based citation extraction ensures accurate source attribution

## Architecture

- `search_engine.py`: Handles SerpAPI integration and result formatting
- `ai_processor.py`: Manages OpenAI API calls and citation extraction
- `cli.py`: Main entry point with CLI logic and display formatting

## Future Improvements

With more time, I would add:
- **Caching**: Cache search results and AI responses to reduce API calls
- **Multiple Search Engines**: Add support for Bing, DuckDuckGo, etc.
- **Streaming Responses**: Stream AI responses as they're generated
- **Export Functionality**: Save responses to markdown/PDF
- **Advanced Queries**: Support for filters, date ranges, and site-specific searches
- **Local LLM Option**: Support for Ollama or other local models
- **Web UI**: Simple Flask/FastAPI web interface
- **Tests**: Comprehensive test suite with mocked API responses