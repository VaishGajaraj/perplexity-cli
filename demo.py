#!/usr/bin/env python3
"""
Demo script to showcase Perplexity CLI functionality
"""

import subprocess
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def run_demo():
    console.print(Panel.fit(
        "[bold cyan]🔍 Perplexity CLI Demo[/bold cyan]\n\n"
        "AI-powered search with real-time web results and citations",
        border_style="cyan"
    ))
    
    # Sample queries to demonstrate different capabilities
    queries = [
        {
            "query": "What are the latest developments in quantum computing in 2024?",
            "description": "Current events and technology updates"
        },
        {
            "query": "Explain the differences between Python async and threading",
            "description": "Technical programming concepts"
        },
        {
            "query": "What are the health benefits of intermittent fasting?",
            "description": "Health and science information"
        }
    ]
    
    console.print("\n[bold]📋 Demo Queries:[/bold]")
    for i, q in enumerate(queries, 1):
        console.print(f"{i}. [cyan]{q['query']}[/cyan]")
        console.print(f"   [dim]{q['description']}[/dim]")
    
    console.print("\n[yellow]Note: Make sure you have set up your API keys in .env file[/yellow]\n")
    
    for i, query_info in enumerate(queries, 1):
        console.rule(f"[bold]Query {i} of {len(queries)}[/bold]", style="blue")
        console.print(f"\n[bold cyan]Query:[/bold cyan] {query_info['query']}")
        console.print(f"[dim]Category: {query_info['description']}[/dim]\n")
        
        # Run the CLI with the query
        cmd = ["python", "cli.py", "-q", query_info['query'], "-r", "3"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Only show the output, not the full stdout
            if result.returncode == 0:
                console.print("[green]✓ Query completed successfully[/green]")
            else:
                console.print(f"[red]✗ Query failed with error:[/red]")
                if result.stderr:
                    console.print(result.stderr)
        except Exception as e:
            console.print(f"[red]Failed to run query: {e}[/red]")
        
        # Pause between queries
        if i < len(queries):
            console.print("\n[dim]Press Enter to continue to the next query...[/dim]")
            input()
    
    # Show summary
    console.rule("[bold green]✅ Demo Completed![/bold green]", style="green")
    
    console.print(Panel(
        "[bold]Try the CLI yourself:[/bold]\n\n"
        "[cyan]Interactive mode:[/cyan]\n"
        "  python cli.py\n\n"
        "[cyan]Direct query:[/cyan]\n"
        "  python cli.py -q 'your question here'\n\n"
        "[cyan]With options:[/cyan]\n"
        "  python cli.py -q 'your question' -r 10 --no-cache\n"
        "  python cli.py -q 'your question' -m gpt-4o\n\n"
        "[cyan]Clear cache:[/cyan]\n"
        "  python cli.py --clear-cache",
        title="[bold]Next Steps[/bold]",
        border_style="green"
    ))

if __name__ == "__main__":
    run_demo()