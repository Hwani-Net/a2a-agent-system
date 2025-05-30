#!/usr/bin/env python3
"""
Test Code Generation Feature
"""
import requests
import json

def test_code_generation():
    base_url = "http://localhost:8000"
    
    print("🎨 코드 생성 테스트")
    print("=" * 30)
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mgx/generate_artifact",
            "params": {
                "project_id": "test-project",
                "component_type": "React Todo 컴포넌트"
            },
            "id": "5"
        }
        
        response = requests.post(f"{base_url}/a2a", json=payload)
        result = response.json()
        
        print(f"응답: {result}")
        
        if "result" in result and result["result"]:
            artifact = result["result"]["artifact"]
            print(f"✅ 코드 생성 완료!")
            print(f"📝 타입: {artifact['component_type']}")
            print(f"👨‍💻 작성자: {artifact['created_by']}")
            print(f"📅 생성일: {artifact['created_at']}")
            print()
            print("📋 생성된 코드:")
            print(artifact['content'][:500] + "...")
        else:
            print(f"❌ 코드 생성 실패: {result}")
    
    except Exception as e:
        print(f"❌ 에러: {e}")

if __name__ == "__main__":
    test_code_generation() 