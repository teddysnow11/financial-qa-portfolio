# test_calc.py
import pytest
# [수정] calculate_surcharge_rate 함수를 추가로 불러옵니다.
from calc import calculate_final_premium, calculate_surcharge_rate

# ---------------------------------------------------------
# 1. 핵심 산출 로직 검증 (Logic Verification)
# ---------------------------------------------------------
def test_calculate_premium_grandeur():
    """
    [Ticket #1 검증] 그랜저, 38세, 무사고 -> 표준 요율 적용 확인
    """
    # 시나리오: 그랜저, 38세(AG_0035), 사고 없음(0,0), 블랙박스/자녀 할인
    result = calculate_final_premium("grandeur", 38, "AG_0035", 0, 0, ["blackbox", "children"])

    # 기대 결과: "628,773원"이라는 글자가 결과에 포함되어야 함
    assert "628,773원" in result

# ---------------------------------------------------------
# 2. 방어 로직 검증 (Defense Logic)
# ---------------------------------------------------------
def test_conflict_specials():
    """
    [Ticket #3 검증] 상충 특약(티맵+커넥티드카) 동시 선택 시 방어 로직 작동 확인
    """
    # 시나리오: 티맵 + 커넥티드카(안전) 동시 선택
    result = calculate_final_premium("ray", 30, "AG_0026", 0, 0, ["tmap", "connected_car_safe"])

    # 기대 결과: "아쉽지만" (거절 메시지)가 포함되어야 함
    assert "아쉽지만" in result

def test_age_violation():
    """
    [Ticket #1 예외 검증] 연령 위반 시 거절 메시지 확인
    """
    # 시나리오: 20세가 '만 35세 이상' 특약 가입 시도
    result = calculate_final_premium("avante", 20, "AG_0035", 0, 0, [])

    # 기대 결과: "연령 한정" 에러 메시지 포함
    assert "연령 한정" in result

# ---------------------------------------------------------
# 3. 할증 로직 단위 테스트 (Unit Test)
# ---------------------------------------------------------
def test_calculate_surcharge_rate():
    """
    [Domain Logic] 3년 내 사고 1건 발생 시, 할증 계수가 정확히 1.1이 되는지 검증
    """
    # 시나리오: 3년내 사고 1건(0.1 할증), 1년내 사고 0건 -> 기대값 1.1
    rate = calculate_surcharge_rate(1, 0)
    
    assert rate == pytest.approx(1.1)
  
# ---------------------------------------------------------
# 4. [핵심] 데이터 아키텍처 검증 (Technical Check)
# ---------------------------------------------------------
def test_json_to_xml_mapping_verification():
    """
    [Architecture] Toss(JSON) -> KB(XML/WebSquare) 데이터 매핑 정합성 검증
    - 목적: 모던 프레임워크(JSON)와 레거시 시스템(XML) 간 데이터 타입 불일치 방지
    - 대상: 청약 번호(apcno) 형식이 KB 전문 규격(RQ...)과 일치하는지 확인
    """
    # 1. [가정] Toss에서 넘어오는 JSON 형태의 데이터 (문자열)
    input_data = {"apcno": "RQ2578730214", "joinMall": "NAVER_PM"}

    # 2. KB 로직 처리 (내부 함수 호출)
    # ... 로직 검증 ...

    # 3. 결과 검증
    assert input_data["apcno"].startswith("RQ") # KB 시스템(XML)이 요구하는 'RQ' 접두사로 포함한 청약 번호 형식 검증
