import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI
import re

class AIProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def score_source_quality(self, source: Dict[str, Any]) -> float:
        """Score source quality based on various factors"""
        score = 0.5  # Base score
        
        # Domain authority scoring
        trusted_domains = ['.gov', '.edu', '.org', 'wikipedia.org', 'reuters.com', 
                          'apnews.com', 'bbc.com', 'nytimes.com', 'nature.com']
        domain = source.get('link', '').lower()
        for trusted in trusted_domains:
            if trusted in domain:
                score += 0.3
                break
        
        # Recency scoring
        if source.get('date'):
            score += 0.1
        
        # Content relevance (longer snippets usually more informative)
        snippet_length = len(source.get('snippet', ''))
        if snippet_length > 150:
            score += 0.1
        
        return min(score, 1.0)
    
    def generate_response_with_citations_stream(self, query: str, search_results: List[Dict[str, Any]], model: str = "gpt-4o-mini"):
        """
        Generate an AI response based on search results with citations, streaming the output.
        """
        # Score and sort search results by quality
        scored_results = []
        for result in search_results:
            score = self.score_source_quality(result)
            scored_results.append({**result, 'quality_score': score})
        
        # Sort by quality score descending
        scored_results.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # Create context from search results with quality indicators
        context_parts = []
        for result in scored_results:
            quality_indicator = "⭐" if result['quality_score'] > 0.7 else ""
            context_parts.append(
                f"[{result['index']}] {result['title']} {quality_indicator}\n"
                f"Source: {result['source']}\n"
                f"Content: {result['snippet']}\n"
                f"URL: {result['link']}\n"
                f"Quality Score: {result['quality_score']:.2f}\n"
            )
        
        context = "\n".join(context_parts)
        
        system_prompt = """You are a helpful AI assistant that provides comprehensive answers based on search results. 
        You must cite your sources using [number] format inline with your response.
        Always base your answers on the provided search results and cite them appropriately.
        Pay special attention to sources marked with ⭐ as they have higher quality scores.
        If the search results don't contain enough information, acknowledge this limitation.
        Format your response in a clear, well-structured manner."""
        
        user_prompt = f"""Query: {query}

Search Results:
{context}

Please provide a comprehensive answer to the query based on these search results. 
Include inline citations [1], [2], etc. when referencing specific information from the search results.
Make sure to synthesize information from multiple sources when relevant."""

        try:
            response_stream = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[bold red]Error calling OpenAI API: {e}[/bold red]"

    def generate_follow_up_questions(self, query: str, search_results: List[Dict[str, Any]], model: str = "gpt-4o-mini") -> List[str]:
        """
        Generate a list of relevant follow-up questions.
        """
        context = "\n".join([f"[{res['index']}] {res['snippet']}" for res in search_results])
        
        system_prompt = """You are an AI assistant that generates relevant follow-up questions based on a user's query and the search results. 
        Provide a list of 3-5 insightful questions that the user might ask next. 
        Return the questions as a numbered list."""
        
        user_prompt = f"""Query: {query}

Search Results:
{context}

Based on the above, what are some relevant follow-up questions?"""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            # Use regex to find numbered list items
            questions = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', content, re.DOTALL)
            return [q.strip() for q in questions]
        except Exception as e:
            return [f"Error generating follow-up questions: {e}"]
