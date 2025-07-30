"""Agent mode for autonomous multi-step research"""

from typing import List, Dict, Any
import re

class ResearchAgent:
    def __init__(self, search_engine, ai_processor):
        self.search_engine = search_engine
        self.ai_processor = ai_processor
        self.research_depth = 0
        self.max_depth = 3
        self.context_history = []
    
    def should_deep_research(self, query: str, initial_results: List[Dict]) -> bool:
        """Decide if we need to do deeper research"""
        # Complex queries that need multi-step research
        complex_indicators = [
            'how does', 'explain', 'compare', 'analyze', 
            'what are the implications', 'why does'
        ]
        
        # Check if query is complex
        query_lower = query.lower()
        is_complex = any(indicator in query_lower for indicator in complex_indicators)
        
        # Check if initial results are insufficient
        total_content = sum(len(r.get('snippet', '')) for r in initial_results)
        has_sparse_results = total_content < 500
        
        return is_complex or has_sparse_results
    
    def generate_followup_queries(self, query: str, results: List[Dict], ai_response: str) -> List[str]:
        """Generate follow-up queries for deeper research"""
        # Extract key concepts from AI response
        concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', ai_response)
        
        followups = []
        
        # Generate specific follow-ups based on query type
        if 'how' in query.lower():
            followups.append(f"{query} technical details")
            followups.append(f"{query} step by step process")
        
        if 'compare' in query.lower():
            followups.append(f"{query} advantages disadvantages")
            followups.append(f"{query} real world examples")
        
        # Add concept-specific queries
        for concept in concepts[:2]:  # Limit to top 2 concepts
            followups.append(f"explain {concept} in detail")
        
        return followups[:3]  # Return top 3 follow-ups
    
    def autonomous_research(self, initial_query: str, depth: int = 0) -> Dict[str, Any]:
        """Perform autonomous multi-step research"""
        if depth >= self.max_depth:
            return {"complete": True, "reason": "Max research depth reached"}
        
        # Initial search
        results = self.search_engine.search(initial_query, num_results=5)
        
        # Check if we need deeper research
        if not self.should_deep_research(initial_query, results):
            return {
                "complete": True, 
                "reason": "Sufficient information found",
                "results": results
            }
        
        # Generate AI response
        ai_response = ""
        for chunk in self.ai_processor.generate_response_with_citations_stream(
            initial_query, results
        ):
            ai_response += chunk
        
        # Store context
        self.context_history.append({
            "query": initial_query,
            "response": ai_response,
            "depth": depth
        })
        
        # Generate follow-up queries
        followups = self.generate_followup_queries(initial_query, results, ai_response)
        
        # Research follow-ups
        additional_context = []
        for followup in followups:
            sub_results = self.search_engine.search(followup, num_results=3)
            additional_context.extend(sub_results)
        
        return {
            "complete": False,
            "followup_queries": followups,
            "additional_context": additional_context,
            "depth": depth,
            "should_continue": depth < self.max_depth - 1
        }