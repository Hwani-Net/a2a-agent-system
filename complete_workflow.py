#!/usr/bin/env python3
import requests

def mgx_workflow():
    base_url = "http://localhost:8000"
    
    print("🚀 MGX 완전한 팀 협업 워크플로우")
    print("=" * 50)
    
    # 1. 팀 정보
    print("\n1️⃣ 팀 정보")
    response = requests.post(f"{base_url}/a2a", json={
        "jsonrpc": "2.0", "method": "mgx/team_info", "id": "1"
    })
    team = response.json()["result"]
    print(f"✅ 팀: {team['team_name']} ({len(team['members'])}명)")
    
    # 2. 프로젝트 생성
    print("\n2️⃣ 프로젝트 생성")
    response = requests.post(f"{base_url}/a2a", json={
        "jsonrpc": "2.0",
        "method": "mgx/create_project",
        "params": {"description": "온라인 쇼핑몰 플랫폼"},
        "id": "2"
    })
    project = response.json()["result"]
    project_id = project["project_id"]
    print(f"✅ 프로젝트: {project_id[:8]}... ({project['status']})")
    
    # 3. 코드 생성
    print("\n3️⃣ 코드 생성")
    response = requests.post(f"{base_url}/a2a", json={
        "jsonrpc": "2.0",
        "method": "mgx/generate_artifact",
        "params": {
            "project_id": project_id,
            "component_type": "React 상품 목록"
        },
        "id": "3"
    })
    result = response.json()["result"]
    artifact = result["artifact"]
    print(f"✅ 컴포넌트: {artifact['component_type']}")
    print(f"   작성자: {artifact['created_by']}")
    print(f"   코드 길이: {len(artifact['content'])}자")
    
    print(f"\n🎉 워크플로우 완료! 프로젝트 ID: {project_id}")

if __name__ == "__main__":
    mgx_workflow() 