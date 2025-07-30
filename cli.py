#!/usr/bin/env python3

import click
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
import sys
import re

from search_engine import SearchEngine
from ai_processor import AIProcessor
from cache_manager import CacheManager

# Load environment variables
load_dotenv()

console = Console()

def extract_citations(text: str) -> list[int]:
    """Extract citation numbers from the AI response."""
    citations = list(set(int(match) for match in re.findall(r'\[(\d+)\]', text)))
    citations.sort()
    return citations


@click.command()
@click.option('--query', '-q', help='Search query (if not provided, interactive mode is used)')
@click.option('--results', '-r', default=5, help='Number of search results to fetch')
@click.option('--model', '-m', default='gpt-4o-mini', help='OpenAI model to use')
@click.option('--no-cache', is_flag=True, help='Disable caching')
@click.option('--clear-cache', is_flag=True, help='Clear all cached data')
def main(query, results, model, no_cache, clear_cache):
    """Perplexity CLI - AI-powered search with citations"""
    
    # Check for API keys
    serpapi_key = os.getenv('SERPAPI_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not serpapi_key or not openai_key:
        console.print("[bold red]Error:[/bold red] Missing API keys!")
        console.print("Please set SERPAPI_KEY and OPENAI_API_KEY in your .env file")
        console.print("Copy .env.example to .env and add your keys")
        sys.exit(1)
    
    # Initialize components
    search_engine = SearchEngine(serpapi_key)
    ai_processor = AIProcessor(openai_key)
    cache_manager = CacheManager() if not no_cache else None
    
    # Handle cache clearing
    if clear_cache and cache_manager:
        cache_manager.clear()
        console.print("[green]Cache cleared successfully![/green]")
        if not query:
            sys.exit(0)
    
    # Interactive mode
    if not query:
        console.print("[bold]Welcome to Perplexity CLI![/bold]")
        console.print("Type 'exit' or 'quit' to leave\n")
        
        while True:
            query = Prompt.ask("[bold cyan]Enter your query[/bold cyan]")
            
            if query.lower() in ['exit', 'quit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            process_query(query, results, model, search_engine, ai_processor, cache_manager)
            console.print("\n" + "="*80 + "\n")
    else:
        # Single query mode
        process_query(query, results, model, search_engine, ai_processor, cache_manager)

def process_query(query: str, num_results: int, model: str, search_engine: SearchEngine, ai_processor: AIProcessor, cache_manager: CacheManager = None):
    """Process a single query"""
    
    # Display query
    console.print(f"\n[bold cyan]Query:[/bold cyan] {query}")
    
    # Check cache first
    search_results = None
    ai_response_content = None
    use_cached_ai = False
    
    if cache_manager:
        cached_search = cache_manager.get(query, 'search')
        if cached_search:
            search_results = cached_search
            console.print("[dim]Using cached search results[/dim]")
        
        cached_ai = cache_manager.get(query, 'ai_response')
        if cached_ai and cached_ai.get('model') == model:
            ai_response_content = cached_ai.get('response')
            use_cached_ai = True
            console.print("[dim]Using cached AI response[/dim]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Search if not cached
        if search_results is None:
            search_task = progress.add_task("[cyan]Searching the web...", total=None)
            try:
                search_results = search_engine.search(query, num_results)
                if cache_manager:
                    cache_manager.set(query, 'search', search_results)
                progress.update(search_task, completed=True)
            except Exception as e:
                progress.stop()
                console.print(f"[bold red]Search Error:[/bold red] {str(e)}")
                return
        
    # Generate AI response with streaming (if not cached)
    if not use_cached_ai:
        ai_response_content = ""
        console.print("\n[bold green]AI Response:[/bold green]")
        
        # Check if search results are empty
        if not search_results:
            console.print("[yellow]No search results found. Unable to generate response.[/yellow]")
            return
        
        panel = Panel("Generating response...", title="[bold green]AI Response[/bold green]", border_style="green")
        with Live(panel, console=console, refresh_per_second=4, vertical_overflow="visible") as live:
            try:
                chunk_count = 0
                for chunk in ai_processor.generate_response_with_citations_stream(query, search_results, model):
                    if chunk:  # Only process non-empty chunks
                        ai_response_content += chunk
                        chunk_count += 1
                        # Update the panel with the accumulated content
                        live.update(Panel(ai_response_content, title="[bold green]AI Response[/bold green]", border_style="green"))
                
                if chunk_count == 0:
                    console.print("[yellow]No response generated from AI.[/yellow]")
                    return
                    
            except Exception as e:
                console.print(f"[bold red]AI Error:[/bold red] {str(e)}")
                import traceback
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
                return

        # Cache the AI response if caching is enabled
        if cache_manager and ai_response_content:
            cache_manager.set(query, 'ai_response', {
                'response': ai_response_content,
                'model': model
            })
    else:
        # Display cached response
        console.print("\n[bold green]AI Response:[/bold green]")
        console.print(Panel(ai_response_content, title="[bold green]AI Response (Cached)[/bold green]", border_style="green"))
    
    # Extract citations and display sources
    citations = extract_citations(ai_response_content)
    
    # Display sources cited
    if citations:
        console.print("\n[bold yellow]Sources Used:[/bold yellow]")
        for citation in citations:
            for result in search_results:
                if result['index'] == citation:
                    console.print(f"[{citation}] [link={result['link']}]{result['title']}[/link] - {result['source']}")
    
    # Generate and display follow-up questions
    follow_up_questions = ai_processor.generate_follow_up_questions(query, search_results, model)
    if follow_up_questions:
        console.print("\n[bold yellow]Follow-up Questions:[/bold yellow]")
        for question in follow_up_questions:
            console.print(f"- {question}")

    # Display all search results
    console.print("\n[bold blue]All Search Results:[/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Title", style="white")
    table.add_column("Source", style="green")
    table.add_column("Snippet", style="dim")
    
    for result in search_results:
        table.add_row(
            str(result['index']),
            result['title'][:50] + "..." if len(result['title']) > 50 else result['title'],
            result['source'],
            result['snippet'][:80] + "..." if len(result['snippet']) > 80 else result['snippet']
        )
    
    console.print(table)

if __name__ == '__main__':
    main()

