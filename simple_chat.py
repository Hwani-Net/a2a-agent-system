"""
Simple Interactive A2A Chat Client
"""
import requests
import json
import uuid

class SimpleA2AChat:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.a2a_url = f"{base_url}/a2a"
    
    def send_request(self, method, params=None):
        """Send JSON-RPC request"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": str(uuid.uuid4())
        }
        if params:
            payload["params"] = params
        
        response = requests.post(self.a2a_url, json=payload)
        return response.json()
    
    def chat(self, message):
        """Simple chat function"""
        print(f"You: {message}")
        
        # Create task
        task_result = self.send_request("task/create")
        task_id = task_result.get("result", {}).get("task_id")
        
        if not task_id:
            print("Error: Could not create task")
            return
        
        # Send message
        message_data = {
            "role": "user", 
            "parts": [{"type": "text", "content": message}]
        }
        
        response = self.send_request("task/message", {
            "task_id": task_id,
            "message": message_data
        })
        
        # Extract response
        agent_response = response.get("result", {}).get("response", {})
        if "parts" in agent_response:
            for part in agent_response["parts"]:
                if part.get("type") == "text":
                    print(f"Agent: {part.get('content', '')}")
        else:
            print(f"Agent: {agent_response}")

def main():
    """Interactive chat"""
    chat = SimpleA2AChat()
    
    print("=== Simple A2A Chat ===")
    print("Type 'quit' to exit")
    
    # Test messages
    test_messages = [
        "Hello! Can you introduce yourself?",
        "Generate a short poem about AI",
        "Analyze this text: The future of AI is bright and full of possibilities",
        "Search for machine learning resources"
    ]
    
    print("\n--- Running Test Messages ---")
    for msg in test_messages:
        chat.chat(msg)
        print()
    
    print("--- Interactive Mode ---")
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if user_input:
                chat.chat(user_input)
                print()
        except KeyboardInterrupt:
            break
    
    print("Goodbye!")

if __name__ == "__main__":
    main() 