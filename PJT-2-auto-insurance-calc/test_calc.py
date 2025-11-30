# test_calc.py
import pytest
from calc import calculate_final_premium

def test_calculate_premium_grandeur():
    """
    [Ticket #1 검증] 그랜저, 38세, 무사고 -> 표준 요율 적용 확인
    """
    # 시나리오: 그랜저, 38세(AG_0035), 사고 없음(0,0), 블랙박스/자녀 할인
    result = calculate_final_premium("grandeur", 38, "AG_0035", 0, 0, ["blackbox", "children"])

    # 기대 결과: "628,773원"이라는 글자가 결과에 포함되어야 함
    assert "628,773원" in result

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