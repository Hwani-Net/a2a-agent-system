#!/usr/bin/env python3
"""
Simple test for MGX features using Windows-compatible commands
"""
import requests
import json

def test_server():
    """Test server basic functionality"""
    print("🚀 A2A Server Test with MGX Features")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # 1. Health check
    print("\n1️⃣ Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        health = response.json()
        print(f"✅ Server Status: {health['status']}")
        print(f"   Timestamp: {health['timestamp']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # 2. Agent Card
    print("\n2️⃣ Agent Card")
    try:
        response = requests.get(f"{base_url}/agent-card")
        card = response.json()
        print(f"✅ Agent: {card['identity']['name']}")
        print(f"   Description: {card['identity']['description']}")
        print(f"   Version: {card['identity']['version']}")
        
        # Show MGX team members
        if 'mgx_team_features' in card:
            print("\n👥 MGX Team Members:")
            for member in card['mgx_team_features']['team_members'][:3]:  # Show first 3
                print(f"   {member['avatar']} {member['name']} - {member['role']}")
        
    except Exception as e:
        print(f"❌ Agent card failed: {e}")
        return
    
    # 3. MGX Team Info via A2A
    print("\n3️⃣ MGX Team Info (A2A)")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mgx/team_info",
            "id": "test1"
        }
        
        response = requests.post(f"{base_url}/a2a", json=payload)
        result = response.json()
        
        if 'result' in result:
            team_info = result['result']
            print(f"✅ Team: {team_info['team_name']}")
            print(f"   Description: {team_info['description']}")
            print(f"   Members: {len(team_info['members'])}")
            
            print("\n   Team Members:")
            for member in team_info['members']:
                print(f"   {member['avatar']} {member['name']} ({member['role']})")
        else:
            print(f"❌ A2A Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ MGX team info failed: {e}")
        return
    
    # 4. Create MGX Project
    print("\n4️⃣ Create MGX Project")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mgx/create_project",
            "params": {
                "description": "Create a simple calculator web app",
                "user_id": "test_user"
            },
            "id": "test2"
        }
        
        response = requests.post(f"{base_url}/a2a", json=payload)
        result = response.json()
        
        if 'result' in result:
            project_result = result['result']
            project_id = project_result['project_id']
            print(f"✅ Project Created: {project_id[:8]}...")
            print(f"   Status: {project_result['status']}")
            print(f"   Message: {project_result['message']}")
            
            # 5. Team Discussion
            print("\n5️⃣ Team Discussion")
            payload = {
                "jsonrpc": "2.0",
                "method": "mgx/team_discussion",
                "params": {
                    "project_id": project_id,
                    "topic": "What's the best approach for this calculator?"
                },
                "id": "test3"
            }
            
            response = requests.post(f"{base_url}/a2a", json=payload)
            result = response.json()
            
            if 'result' in result:
                discussion = result['result']
                print(f"✅ Discussion with {discussion['participants']} participants")
                print(f"   Topic: {discussion['topic']}")
                
                print("\n   Team Responses:")
                for response_data in discussion['discussion'][:2]:  # Show first 2
                    agent = response_data['agent']
                    avatar = response_data['avatar']
                    contribution = response_data['contribution'][:80] + "..."
                    print(f"   {avatar} {agent}: {contribution}")
                    
            else:
                print(f"❌ Discussion Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Project Creation Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ MGX project creation failed: {e}")
    
    print("\n🎉 Test completed!")
    print("\n💡 Windows-Compatible Commands:")
    print("   Health Check: python -c \"import requests; print(requests.get('http://localhost:8000/health').json())\"")
    print("   Agent Card:  python -c \"import requests; print(requests.get('http://localhost:8000/agent-card').json())\"")

if __name__ == "__main__":
    test_server() 