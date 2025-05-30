#!/usr/bin/env python3
"""
Quick MGX Test - 핵심 기능만 빠르게 테스트
"""
import requests
import json

def test_mgx_quick():
    base_url = "http://localhost:8000"
    
    print("🚀 Quick MGX Test")
    print("=" * 30)
    
    # 1. 팀 정보
    print("\n1️⃣ 팀 정보")
    try:
        payload = {"jsonrpc": "2.0", "method": "mgx/team_info", "id": "1"}
        response = requests.post(f"{base_url}/a2a", json=payload)
        result = response.json()
        
        print(f"Raw response: {result}")
        
        if "result" in result:
            team = result["result"]
            print(f"✅ 팀: {team['team_name']}")
            print(f"   멤버 수: {len(team['members'])}")
            for member in team['members'][:3]:  # 처음 3명만 출력
                print(f"   {member['avatar']} {member['name']} - {member['role']}")
        else:
            print(f"❌ No result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. 프로젝트 생성
    print("\n2️⃣ 프로젝트 생성")
    try:
        payload = {
            "jsonrpc": "2.0", 
            "method": "mgx/create_project", 
            "params": {"description": "Simple calculator app"}, 
            "id": "2"
        }
        response = requests.post(f"{base_url}/a2a", json=payload)
        result = response.json()
        
        print(f"Raw response: {result}")
        
        if "result" in result:
            project = result["result"]
            project_id = project["project_id"]
            print(f"✅ 프로젝트 생성: {project_id[:8]}...")
            print(f"   상태: {project['status']}")
            
            # 3. 팀 토론
            print("\n3️⃣ 팀 토론")
            payload = {
                "jsonrpc": "2.0",
                "method": "mgx/team_discussion",
                "params": {
                    "project_id": project_id,
                    "topic": "What's the best approach?"
                },
                "id": "3"
            }
            response = requests.post(f"{base_url}/a2a", json=payload)
            result = response.json()
            
            print(f"Raw response: {result}")
            
            if "result" in result:
                discussion = result["result"]
                print(f"✅ 토론 완료! {discussion['participants']}명 참여")
                
                for i, msg in enumerate(discussion['discussion'][:2], 1):
                    print(f"   {i}. {msg['avatar']} {msg['agent']}: {msg['contribution'][:60]}...")
            else:
                print(f"❌ No discussion result: {result}")
        else:
            print(f"❌ No project result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_mgx_quick() 