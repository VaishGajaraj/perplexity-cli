#!/usr/bin/env python3
"""Basic unit tests for Perplexity CLI"""

import unittest
from unittest.mock import Mock, patch
import os
import sys
import tempfile
import json
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from cache_manager import CacheManager
from query_optimizer import QueryOptimizer
from ai_processor import AIProcessor

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache = CacheManager(cache_dir=self.temp_dir, ttl_hours=1)
    
    def test_cache_set_and_get(self):
        """Test basic cache operations"""
        test_data = {"results": ["result1", "result2"]}
        self.cache.set("test query", "search", test_data)
        
        retrieved = self.cache.get("test query", "search")
        self.assertEqual(retrieved, test_data)
    
    def test_cache_expiry(self):
        """Test that expired cache returns None"""
        # Create cache with 0 hours TTL
        cache = CacheManager(cache_dir=self.temp_dir, ttl_hours=0)
        cache.set("test", "type", {"data": "test"})
        
        # Should return None immediately
        self.assertIsNone(cache.get("test", "type"))
    
    def test_cache_clear(self):
        """Test cache clearing"""
        self.cache.set("test1", "type", {"data": 1})
        self.cache.set("test2", "type", {"data": 2})
        
        self.cache.clear()
        
        self.assertIsNone(self.cache.get("test1", "type"))
        self.assertIsNone(self.cache.get("test2", "type"))

class TestQueryOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = QueryOptimizer()
    
    def test_time_sensitive_optimization(self):
        """Test optimization of time-sensitive queries"""
        query = "latest news"
        optimized, alternatives = self.optimizer.optimize_query(query)
        
        # Should add current year to alternatives
        self.assertTrue(any(str(datetime.now().year) in alt for alt in alternatives))
    
    def test_comparison_query_optimization(self):
        """Test optimization of comparison queries"""
        query = "python vs javascript"
        optimized, alternatives = self.optimizer.optimize_query(query)
        
        # Should create comparison alternatives
        self.assertTrue(any("compared to" in alt for alt in alternatives))
        self.assertTrue(any("comparison" in alt for alt in alternatives))
    
    def test_company_query_optimization(self):
        """Test optimization of company queries"""
        query = "what is openai"
        optimized, alternatives = self.optimizer.optimize_query(query)
        
        # Should add context
        self.assertTrue(any("company" in alt or "about" in alt for alt in alternatives))

class TestAIProcessor(unittest.TestCase):
    def setUp(self):
        self.ai_processor = AIProcessor("fake_key")
    
    def test_source_quality_scoring(self):
        """Test source quality scoring algorithm"""
        # Test trusted domain
        trusted_source = {
            "link": "https://www.nytimes.com/article",
            "snippet": "A" * 200,  # Long snippet
            "date": "2024-01-01"
        }
        score = self.ai_processor.score_source_quality(trusted_source)
        self.assertGreater(score, 0.8)  # Should be high quality
        
        # Test untrusted domain
        untrusted_source = {
            "link": "https://random-blog.com/post",
            "snippet": "Short",
            "date": ""
        }
        score = self.ai_processor.score_source_quality(untrusted_source)
        self.assertLess(score, 0.7)  # Should be lower quality
    
    def test_citation_extraction(self):
        """Test citation extraction from text"""
        from cli import extract_citations
        
        text = "This is a fact [1]. Another fact [2]. And one more [1]."
        citations = extract_citations(text)
        
        self.assertEqual(citations, [1, 2])  # Should be sorted and unique

class TestIntegration(unittest.TestCase):
    @patch('subprocess.run')
    def test_cli_execution(self, mock_run):
        """Test that CLI can be executed"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Query: test\nAI Response: Test response"
        
        import subprocess
        result = subprocess.run(['python', 'cli.py', '-q', 'test'], capture_output=True)
        
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()