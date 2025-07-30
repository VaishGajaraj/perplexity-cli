#!/usr/bin/env python3
"""
Demo script to showcase Perplexity CLI functionality
"""

import subprocess
import time
import os
import sys
import re
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live

console = Console()

def clean_ansi_codes(text):
    """Remove ANSI escape codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def extract_sections(output):
    """Extract different sections from the CLI output"""
    sections = {
        'query': '',
        'ai_response': '',
        'sources': [],
        'search_results': []
    }
    
    lines = output.split('\n')
    current_section = None
    ai_response_lines = []
    
    for i, line in enumerate(lines):
        # Extract query
        if line.strip().startswith('Query:'):
            sections['query'] = line.replace('Query:', '').strip()
        
        # Extract AI response
        elif 'AI Response:' in line:
            current_section = 'ai_response'
            # Look for the panel content
            j = i + 1
            while j < len(lines) and 'Sources Used:' not in lines[j]:
                if lines[j].strip() and not lines[j].startswith('⠋'):
                    ai_response_lines.append(lines[j])
                j += 1
        
        # Extract sources
        elif 'Sources Used:' in line:
            current_section = 'sources'
        elif current_section == 'sources' and line.strip().startswith('['):
            sections['sources'].append(line.strip())
        
        # Stop at search results table
        elif 'All Search Results:' in line:
            break
    
    # Clean up AI response
    ai_text = '\n'.join(ai_response_lines)
    # Remove box drawing characters
    ai_text = re.sub(r'[╭╮╰╯│─]', '', ai_text)
    sections['ai_response'] = ai_text.strip()
    
    return sections

def run_demo():
    # Clear screen for better presentation
    console.clear()
    
    # Animated intro
    console.print(Panel(
        "[bold cyan]🔍 Perplexity CLI Demo[/bold cyan]\n\n"
        "[yellow]AI-powered search with real-time web results and citations[/yellow]\n\n"
        "[dim]This demo will show you how the CLI works with real examples[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    time.sleep(2)
    
    # Sample queries with better variety
    queries = [
        {
            "query": "What company is Hanover Park and what do they do?",
            "description": "Company research query",
            "color": "green"
        },
        {
            "query": "Compare Python FastAPI vs Flask for building APIs",
            "description": "Technical comparison query",
            "color": "blue"
        },
        {
            "query": "What are the latest breakthroughs in AI as of 2025?",
            "description": "Current events query",
            "color": "magenta"
        }
    ]
    
    # Show query overview
    console.print("\n[bold]📋 Today's Demo Queries:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta", border_style="blue")
    table.add_column("№", style="cyan", width=3)
    table.add_column("Query", style="white")
    table.add_column("Type", style="yellow")
    
    for i, q in enumerate(queries, 1):
        table.add_row(str(i), q['query'], q['description'])
    
    console.print(table)
    console.print("\n[dim]Starting in 3 seconds...[/dim]")
    time.sleep(3)
    
    # Process each query
    for i, query_info in enumerate(queries, 1):
        console.clear()
        
        # Query header
        console.rule(f"[bold {query_info['color']}]🔍 Query {i} of {len(queries)}[/bold {query_info['color']}]", style=query_info['color'])
        console.print(f"\n[bold {query_info['color']}]Query:[/bold {query_info['color']}] {query_info['query']}")
        console.print(f"[dim]Type: {query_info['description']}[/dim]\n")
        
        # Run the query with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Running query...", total=None)
            
            cmd = ["python", "cli.py", "-q", query_info['query'], "-r", "3"]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                progress.update(task, completed=True)
                
                if result.returncode == 0:
                    # Parse and display the output
                    sections = extract_sections(result.stdout)
                    
                    # Show AI Response
                    if sections['ai_response']:
                        console.print("\n[bold green]✨ AI Response:[/bold green]")
                        console.print(Panel(
                            Markdown(sections['ai_response']),
                            border_style="green",
                            padding=(1, 2)
                        ))
                    
                    # Show sources
                    if sections['sources']:
                        console.print("\n[bold yellow]📚 Sources Used:[/bold yellow]")
                        for source in sections['sources']:
                            console.print(f"  {source}")
                    
                    # Success message
                    console.print("\n[bold green]✓ Query completed successfully![/bold green]")
                    
                else:
                    console.print(f"\n[red]✗ Query failed[/red]")
                    if result.stderr:
                        console.print(Panel(result.stderr, title="Error", border_style="red"))
                        
            except subprocess.TimeoutExpired:
                console.print("\n[red]✗ Query timed out after 30 seconds[/red]")
            except Exception as e:
                console.print(f"\n[red]✗ Error: {e}[/red]")
        
        # Pause between queries
        if i < len(queries):
            console.print(f"\n[dim]Press Enter to see query {i+1} of {len(queries)}...[/dim]")
            input()
    
    # Final summary
    console.clear()
    console.rule("[bold green]✅ Demo Complete![/bold green]", style="green")
    
    # Features showcase
    console.print("\n[bold]🌟 Features Demonstrated:[/bold]\n")
    
    features = [
        ("🔍", "Real-time web search", "Fetches current information from Google"),
        ("🤖", "AI synthesis", "GPT-4 analyzes and summarizes search results"),
        ("📎", "Smart citations", "Every claim is backed by numbered sources"),
        ("💾", "Intelligent caching", "Reduces API costs and improves speed"),
        ("🎨", "Beautiful UI", "Rich terminal formatting with live updates"),
        ("❓", "Follow-up questions", "AI suggests related queries"),
    ]
    
    for emoji, feature, description in features:
        console.print(f"  {emoji} [bold cyan]{feature}[/bold cyan]")
        console.print(f"     [dim]{description}[/dim]")
    
    # Command examples
    console.print("\n" + "─" * 80 + "\n")
    
    console.print(Panel(
        "[bold]🚀 Ready to try it yourself?[/bold]\n\n"
        "[yellow]Interactive mode:[/yellow]\n"
        "  $ python cli.py\n\n"
        "[yellow]Quick search:[/yellow]\n"
        "  $ python cli.py -q 'your question here'\n\n"
        "[yellow]Advanced options:[/yellow]\n"
        "  $ python cli.py -q 'complex query' -r 10 -m gpt-4o\n"
        "  $ python cli.py -q 'latest news' --no-cache\n"
        "  $ python cli.py --clear-cache\n\n"
        "[dim]Tip: Use -r to control number of search results (default: 5)[/dim]\n"
        "[dim]Tip: Use -m gpt-4o for better quality on complex queries[/dim]",
        title="[bold]Command Reference[/bold]",
        border_style="green",
        padding=(1, 2)
    ))
    
    console.print("\n[bold cyan]Thank you for watching the demo! 🎉[/bold cyan]\n")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
        sys.exit(0)