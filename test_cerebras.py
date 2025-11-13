"""
Quick test script to verify Cerebras integration.
"""

import os
from dotenv import load_dotenv
from agent.cerebras_client import CerebrasClient

# Load environment variables
load_dotenv()

def test_cerebras_client():
    """Test basic Cerebras client functionality."""
    
    print("Testing Cerebras Client Integration...")
    print("-" * 50)
    
    # Check API key
    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        print("❌ CEREBRAS_API_KEY not found in environment")
        print("Please set it in your .env file")
        return False
    
    print(f"✓ API key found: {api_key[:10]}...")
    
    # Initialize client
    try:
        client = CerebrasClient(api_key)
        print(f"✓ Client initialized with model: {client.model}")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test simple completion
    print("\nTesting simple completion...")
    try:
        messages = [
            {"role": "user", "content": "Say 'Hello from Cerebras!' and nothing else."}
        ]
        
        response = client.create_chat_completion(messages=messages, stream=False)
        
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            print(f"✓ Response received: {content}")
        else:
            print(f"❌ Unexpected response format: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Completion failed: {e}")
        return False
    
    # Test streaming
    print("\nTesting streaming completion...")
    try:
        messages = [
            {"role": "user", "content": "Count from 1 to 3, one number per line."}
        ]
        
        print("Stream output: ", end="")
        for chunk in client.create_chat_completion(messages=messages, stream=True):
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    print(content, end="", flush=True)
        
        print("\n✓ Streaming completed successfully")
        
    except Exception as e:
        print(f"\n❌ Streaming failed: {e}")
        return False
    
    print("\n" + "-" * 50)
    print("✅ All tests passed! Cerebras integration is working.")
    return True

if __name__ == "__main__":
    test_cerebras_client()
