#!/usr/bin/env python3
"""Test OpenAI API connection"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def test_openai():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    print(f"API Key found: {api_key[:10]}...")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one word."}
            ],
            max_tokens=10
        )
        
        print(f"Success! Response: {response.choices[0].message.content}")
        
        # Test streaming
        print("\nTesting streaming...")
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            stream=True,
            max_tokens=50
        )
        
        print("Streaming response: ", end="")
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_openai()