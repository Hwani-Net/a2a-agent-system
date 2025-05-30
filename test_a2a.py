"""
Simple A2A JSON-RPC Test
"""
import requests
import json

def test_a2a_endpoint():
    """Direct test of A2A JSON-RPC endpoint"""
    
    # Test 1: Create Task
    print("=== Testing Task Creation ===")
    payload = {
        "jsonrpc": "2.0",
        "method": "task/create", 
        "id": "test1"
    }
    
    try:
        response = requests.post("http://localhost:8000/a2a", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("result", {}).get("task_id")
            print(f"Task ID: {task_id}")
            
            # Test 2: Send Message
            if task_id:
                print("\n=== Testing Message Send ===")
                message_payload = {
                    "jsonrpc": "2.0", 
                    "method": "task/message",
                    "params": {
                        "task_id": task_id,
                        "message": {
                            "role": "user",
                            "parts": [{"type": "text", "content": "Hello, please introduce yourself!"}]
                        }
                    },
                    "id": "test2"
                }
                
                msg_response = requests.post("http://localhost:8000/a2a", json=message_payload)
                print(f"Status: {msg_response.status_code}")
                print(f"Response: {msg_response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_a2a_endpoint() 