#!/usr/bin/env python3
"""
Test script for Crew Sync Agent MCP server
"""

import json
import subprocess
import sys

def run_mcp_test(request_data, test_name):
    """Run a single MCP test"""
    print(f"\n🔍 {test_name}...")
    
    try:
        request_json = json.dumps(request_data)
        
        process = subprocess.run(
            [sys.executable, "mcp_server.py"],
            input=request_json,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        if process.returncode == 0:
            print("✅ 성공!")
            try:
                response = json.loads(process.stdout.strip().split('\n')[-1])
                if 'result' in response:
                    content = response['result'].get('content', [])
                    if content and len(content) > 0:
                        print(f"\n📋 결과:")
                        print("=" * 60)
                        print(content[0].get('text', ''))
                        print("=" * 60)
                return True
            except Exception as e:
                print(f"응답 파싱 오류: {e}")
                print(f"원시 응답: {process.stdout.strip()}")
        else:
            print(f"❌ 실패: {process.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return False

def test_crew_sync_agent():
    """Test the Crew Sync Agent comprehensively"""
    print("🚀 Crew Sync Agent 종합 테스트 시작\n")
    
    # Test 1: List current crew
    test1_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "list_crew",
            "arguments": {}
        }
    }
    run_mcp_test(test1_request, "현재 크루 멤버 조회")
    
    # Test 2: Add new crew member
    test2_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "add_crew_member",
            "arguments": {
                "name": "Alex",
                "role": "Security Specialist - Cybersecurity and compliance expert"
            }
        }
    }
    run_mcp_test(test2_request, "새 크루 멤버 추가 (Alex)")
    
    # Test 3: Sync crew with default members
    test3_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "sync_crew",
            "arguments": {
                "task": "모바일 앱을 위한 AI 기반 작업 관리 시스템 개발",
                "priority": "high"
            }
        }
    }
    run_mcp_test(test3_request, "기본 크루와 동기화")
    
    # Test 4: Sync crew with specific members
    test4_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "sync_crew",
            "arguments": {
                "task": "데이터베이스 최적화 및 성능 튜닝",
                "crew_members": ["Jordan", "Casey", "Morgan"],
                "priority": "urgent"
            }
        }
    }
    run_mcp_test(test4_request, "특정 크루 멤버와 동기화")
    
    # Test 5: Echo test
    test5_request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {
                "text": "Crew Sync Agent가 정상적으로 작동합니다!"
            }
        }
    }
    run_mcp_test(test5_request, "Echo 테스트")
    
    print("\n🎉 모든 테스트가 완료되었습니다!")

if __name__ == "__main__":
    test_crew_sync_agent() 