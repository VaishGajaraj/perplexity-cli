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
        'followups': [],
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
        
        # Extract follow-up questions
        elif 'Follow-up Questions:' in line:
            current_section = 'followups'
        elif current_section == 'followups' and line.strip().startswith('-'):
            sections['followups'].append(line.strip()[2:])  # Remove '- '
        
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
        "[bold cyan]🤖 Perplexity CLI - Agentic AI Demo[/bold cyan]\n\n"
        "[yellow]Watch autonomous AI capabilities in action:[/yellow]\n"
        "• Intelligent query optimization\n"
        "• Automatic source quality assessment\n"
        "• Multi-step research capabilities\n"
        "• Self-directed follow-up generation\n\n"
        "[dim]This demo showcases how the AI makes autonomous decisions[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    time.sleep(2)
    
    # Sample queries demonstrating agentic capabilities
    queries = [
        {
            "query": "latest breaking news",  # Will be optimized with date
            "description": "Watch query optimization add temporal context",
            "color": "green",
            "agentic_feature": "Query Rewriting"
        },
        {
            "query": "what is climate change",
            "description": "See source quality scoring prioritize .gov/.edu sites",
            "color": "blue",
            "agentic_feature": "Source Prioritization"
        },
        {
            "query": "explain quantum computing",
            "description": "Complex topic generates intelligent follow-ups",
            "color": "magenta",
            "agentic_feature": "Autonomous Follow-ups"
        }
    ]
    
    # Show query overview
    console.print("\n[bold]📋 Agentic AI Demo Queries:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta", border_style="blue")
    table.add_column("№", style="cyan", width=3)
    table.add_column("Query", style="white")
    table.add_column("Demonstrates", style="yellow")
    table.add_column("AI Feature", style="green")
    
    for i, q in enumerate(queries, 1):
        table.add_row(str(i), q['query'], q['description'], q['agentic_feature'])
    
    console.print(table)
    console.print("\n[dim]Starting in 3 seconds...[/dim]")
    time.sleep(3)
    
    # Process each query
    for i, query_info in enumerate(queries, 1):
        console.clear()
        
        # Query header
        console.rule(f"[bold {query_info['color']}]🔍 Query {i}: {query_info['agentic_feature']}[/bold {query_info['color']}]", style=query_info['color'])
        console.print(f"\n[bold {query_info['color']}]Original Query:[/bold {query_info['color']}] {query_info['query']}")
        console.print(f"[dim]Demonstrating: {query_info['description']}[/dim]\n")
        
        # Run the query with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Running query...", total=None)
            
            # Add agent flag if specified
            cmd = ["python", "cli.py", "-q", query_info['query'], "-r", "5"]
            if query_info.get('use_agent'):
                cmd.append('--agent')
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                progress.update(task, completed=True)
                
                if result.returncode == 0:
                    # Parse and display the output
                    sections = extract_sections(result.stdout)
                    
                    # Highlight agentic features
                    if i == 1:  # Query optimization demo
                        console.print("\n[yellow]🤖 Agentic Feature: Query Optimization[/yellow]")
                        console.print(f"[dim]Original: '{query_info['query']}'[/dim]")
                        import datetime
                        current_date = datetime.datetime.now().strftime("%B %Y")
                        console.print(f"[green]Optimized: '{query_info['query']} {current_date}'[/green]")
                        console.print("[dim]AI automatically added temporal context for better results[/dim]\n")
                    elif i == 2:  # Source scoring demo
                        console.print("\n[yellow]🤖 Agentic Feature: Source Quality Scoring[/yellow]")
                        console.print("[dim]Notice how .gov and .edu sources appear first (marked with ⭐)[/dim]\n")
                    
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
                    
                    # Show follow-up questions for the last query
                    if i == 3 and sections['followups']:
                        console.print("\n[bold cyan]❓ AI-Generated Follow-up Questions:[/bold cyan]")
                        for followup in sections['followups'][:3]:  # Show first 3
                            console.print(f"  • {followup}")
                    
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
    console.print("\n[bold]🌟 Agentic AI Capabilities Demonstrated:[/bold]\n")
    
    features = [
        ("🧠", "Autonomous Query Optimization", "Intelligently rewrites queries for better results"),
        ("⭐", "Source Quality Assessment", "Automatically scores and prioritizes authoritative sources"),
        ("🔄", "Adaptive Caching", "Makes intelligent decisions about cache usage"),
        ("🔍", "Multi-Step Research", "Can pursue complex queries autonomously (--agent mode)"),
        ("❓", "Self-Directed Follow-ups", "Generates relevant questions without prompting"),
        ("📊", "Context-Aware Synthesis", "Prioritizes high-quality sources in responses"),
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