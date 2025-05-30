"""
Test MGX-Inspired Features in A2A System
"""
import asyncio
import json
from a2a_client import A2AClient

async def test_mgx_features():
    """Test the new MGX-inspired team features"""
    client = A2AClient("http://localhost:8000")
    
    print("🚀 Testing MGX-Inspired A2A Team Features")
    print("=" * 50)
    
    # Test 1: Get team information
    print("\n1️⃣ Getting Team Information")
    try:
        team_info = client.send_jsonrpc_request("mgx/team_info")
        print(f"Team: {team_info['team_name']}")
        print(f"Description: {team_info['description']}")
        print("\nTeam Members:")
        for member in team_info['members']:
            print(f"  {member['avatar']} {member['name']} ({member['role']})")
            print(f"     {member['description']}")
            print(f"     Specialties: {', '.join(member['specialties'])}")
            print()
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Create a project
    print("\n2️⃣ Creating MGX Project")
    project_description = "Create a modern task management web application with drag-and-drop functionality, user authentication, team collaboration, and real-time updates"
    
    try:
        project_result = client.send_jsonrpc_request("mgx/create_project", {
            "description": project_description,
            "user_id": "test_user_123"
        })
        
        project_id = project_result["project_id"]
        print(f"✅ Project created: {project_id}")
        print(f"Status: {project_result['status']}")
        print(f"Message: {project_result['message']}")
        
        # Test 3: Get project status
        print("\n3️⃣ Getting Project Status")
        status = client.send_jsonrpc_request("mgx/project_status", {
            "project_id": project_id
        })
        print(f"Project Title: {status['title']}")
        print(f"Status: {status['status']}")
        print(f"Assigned Agents: {', '.join(status['assigned_agents'])}")
        print(f"Created: {status['created_at']}")
        
        # Test 4: Team discussion
        print("\n4️⃣ Starting Team Discussion")
        discussion_result = client.send_jsonrpc_request("mgx/team_discussion", {
            "project_id": project_id,
            "topic": "Let's discuss the technical architecture and choose the best tech stack for this project"
        })
        
        print(f"Discussion Topic: {discussion_result['topic']}")
        print(f"Participants: {discussion_result['participants']}")
        print("\nTeam Discussion:")
        for response in discussion_result['discussion']:
            print(f"\n{response['avatar']} {response['agent']} ({response['role']}):")
            print(f"  {response['contribution']}")
        
        # Test 5: Generate code artifact
        print("\n5️⃣ Generating Code Artifact")
        artifact_result = client.send_jsonrpc_request("mgx/generate_artifact", {
            "project_id": project_id,
            "component_type": "React Task Component"
        })
        
        artifact = artifact_result["artifact"]
        print(f"✅ {artifact_result['message']}")
        print(f"Artifact ID: {artifact['id']}")
        print(f"Type: {artifact['component_type']}")
        print(f"Created by: {artifact['created_by']}")
        print(f"Version: {artifact['version']}")
        print("\nCode Preview (first 300 chars):")
        print("-" * 40)
        print(artifact['content'][:300] + "...")
        print("-" * 40)
        
        # Test 6: Another team discussion 
        print("\n6️⃣ Follow-up Team Discussion")
        discussion_result2 = client.send_jsonrpc_request("mgx/team_discussion", {
            "project_id": project_id,
            "topic": "Let's review the generated code and discuss any improvements or additional features needed"
        })
        
        print(f"Discussion Topic: {discussion_result2['topic']}")
        print("\nTeam Discussion:")
        for response in discussion_result2['discussion']:
            print(f"\n{response['avatar']} {response['agent']}:")
            print(f"  {response['contribution']}")
        
        # Test 7: Final project status
        print("\n7️⃣ Final Project Status")
        final_status = client.send_jsonrpc_request("mgx/project_status", {
            "project_id": project_id
        })
        print(f"Artifacts Created: {final_status['artifacts_count']}")
        print(f"Conversation Messages: {final_status['conversation_messages']}")
        print(f"Latest Activity: {final_status['latest_activity']}")
        
    except Exception as e:
        print(f"❌ Error during project workflow: {e}")

def simple_mgx_demo():
    """Simple demo without async"""
    client = A2AClient("http://localhost:8000")
    
    print("🎯 Quick MGX Demo")
    print("=" * 30)
    
    # Quick team info
    print("\n👥 Team:")
    try:
        team_info = client.send_jsonrpc_request("mgx/team_info")
        for member in team_info['members']:
            print(f"  {member['avatar']} {member['name']} - {member['role']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Create simple project
    print("\n🚀 Creating Project...")
    try:
        result = client.send_jsonrpc_request("mgx/create_project", {
            "description": "Build a simple calculator web app"
        })
        project_id = result["project_id"]
        print(f"✅ Project created: {project_id[:8]}...")
        
        # Quick discussion
        print("\n💬 Team Discussion...")
        discussion = client.send_jsonrpc_request("mgx/team_discussion", {
            "project_id": project_id,
            "topic": "What's the best approach for this calculator app?"
        })
        
        for response in discussion['discussion'][:2]:  # Show first 2 responses
            print(f"  {response['avatar']} {response['agent']}: {response['contribution'][:80]}...")
        
        print(f"\n✨ Success! Full team discussion with {len(discussion['discussion'])} participants")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        simple_mgx_demo()
    else:
        asyncio.run(test_mgx_features()) 