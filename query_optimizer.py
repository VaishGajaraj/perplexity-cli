"""Query optimization for better search results"""

import re
from typing import List, Tuple
from datetime import datetime

class QueryOptimizer:
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().strftime("%B")
    
    def optimize_query(self, original_query: str) -> Tuple[str, List[str]]:
        """
        Optimize query for better search results
        Returns: (optimized_query, list_of_alternative_queries)
        """
        query = original_query.lower().strip()
        alternatives = []
        
        # Time-sensitive optimization
        time_keywords = ['latest', 'recent', 'current', 'today', 'now', 'trending']
        if any(keyword in query for keyword in time_keywords):
            # Add current time context
            if 'latest' in query or 'recent' in query:
                alternatives.append(f"{original_query} {self.current_month} {self.current_year}")
            if 'today' in query or 'now' in query:
                alternatives.append(f"{original_query} {self.current_month} {self.current_year}")
        
        # Technical query optimization
        if any(tech in query for tech in ['vs', 'versus', 'compare', 'difference between']):
            # Reformat comparison queries
            parts = re.split(r'\s+vs\s+|\s+versus\s+|difference between\s+', query)
            if len(parts) >= 2:
                alternatives.append(f"{parts[0].strip()} compared to {parts[1].strip()}")
                alternatives.append(f"{parts[0].strip()} {parts[1].strip()} comparison")
        
        # Company/product queries
        if 'what is' in query or 'who is' in query:
            # Add context words for better results
            entity = query.replace('what is', '').replace('who is', '').strip()
            alternatives.append(f"{entity} company overview")
            alternatives.append(f"{entity} about information")
        
        # News queries
        news_keywords = ['news', 'headlines', 'breaking', 'events']
        if any(keyword in query for keyword in news_keywords):
            # Make news queries more specific
            if 'news' in query and not any(str(year) in query for year in range(2020, 2026)):
                alternatives.append(f"{original_query} {self.current_year}")
            alternatives.append(original_query.replace('news', 'latest news updates'))
        
        # Question queries
        question_words = ['how', 'why', 'when', 'where', 'what']
        if any(query.startswith(word) for word in question_words):
            # Add "explained" or "guide" for better educational content
            alternatives.append(f"{original_query} explained")
            alternatives.append(f"{original_query} complete guide")
        
        # Always include the original query
        return original_query, alternatives[:3]  # Limit to 3 alternatives
    
    def should_use_alternatives(self, query: str) -> bool:
        """Determine if we should try alternative queries"""
        # Use alternatives for vague or general queries
        vague_indicators = ['latest', 'news', 'trending', 'current', 'what is', 'how to']
        return any(indicator in query.lower() for indicator in vague_indicators)