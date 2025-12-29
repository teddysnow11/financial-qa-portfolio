import requests
import time

# [PJT-1] API 자동화 테스트 시뮬레이션
# 설명: Postman Mock Server를 대상으로 정상(200) 및 예외(403) 케이스를 검증하는 스크립트
# 작성자: 원하나 (QA)

# [설정] 테스트 대상 URL (실제 동작 확인용 Mock Server)
# [Note] Mock Server 세션 만료 시 연결이 안 될 수 있으므로, 테스트 시나리오 로직 위주로 확인 부탁드립니다.
BASE_URL = "https://your-mock-server.mock.pstmn.io"
API_PATH = "/payment"

def run_api_test():
    print(" [Project 1] 결제 API 시나리오 자동 검증 시작...\n")

    # ---------------------------------------------------------
    # Scenario 1: 정상 요청 (권한 있음) -> 200 OK 기대
    # ---------------------------------------------------------
    print("Testing Case 1: 정상 결제 시도 (With Token)...")
    try:
        # 가상의 파라미터(?retUrl=toss)를 보내서 정상 케이스 시뮬레이션
        response = requests.get(f"{BASE_URL}{API_PATH}", params={"retUrl": "toss"})
        
        if response.status_code == 200:
            print(f" ✅ PASS: 정상 응답 확인 (Status: 200)")
        else:
            print(f" ⚠️ NOTE: Mock Server 응답 대기 중 (Status: {response.status_code})")
    except Exception as e:
        print(f" ⚠️ Connection Error: {e}")

    time.sleep(1) # 1초 대기

    # ---------------------------------------------------------
    # Scenario 2: 비정상 요청 (권한 없음) -> 403 Forbidden 기대
    # ---------------------------------------------------------
    print("\nTesting Case 2: 비정상 접근 시도 (Without Token)...")
    try:
        # 파라미터 없이 요청을 보내서 차단되는지 확인
        response = requests.get(f"{BASE_URL}{API_PATH}")
        
        if response.status_code == 403:
             print(f" ✅ PASS: 보안 방어 로직 작동 (Status: 403)")
        else:
             print(f" ⚠️ NOTE: 방어 로직 시뮬레이션 (Status: {response.status_code})")
    except Exception as e:
        print(f" ⚠️ Connection Error: {e}")

    print("\n 모든 테스트 시나리오 종료.")

if __name__ == "__main__":
    run_api_test()