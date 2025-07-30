import os
from typing import List, Dict, Any
from serpapi import GoogleSearch
from datetime import datetime

class SearchEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search using SerpAPI
        """
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": num_results,
            "hl": "en",
            "gl": "us"
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "error" in results:
                raise Exception(results["error"])
            
            formatted_results = []
            
            # Process organic results
            if "organic_results" in results:
                for idx, result in enumerate(results["organic_results"][:num_results]):
                    formatted_results.append({
                        "index": idx + 1,
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "source": result.get("source", result.get("link", "").split("/")[2] if "/" in result.get("link", "") else ""),
                        "date": result.get("date", "")
                    })
            
            # Add answer box if available
            if "answer_box" in results:
                answer_box = results["answer_box"]
                formatted_results.insert(0, {
                    "index": 0,
                    "title": "Featured Answer",
                    "link": answer_box.get("link", ""),
                    "snippet": answer_box.get("answer", answer_box.get("snippet", "")),
                    "source": "Answer Box",
                    "date": ""
                })
            
            return formatted_results
        except Exception as e:
            raise Exception(f"An error occurred during the search: {e}")
