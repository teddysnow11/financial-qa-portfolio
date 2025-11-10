# test_car_logic_v1.py

# [1. '자동차할인특약 - 자녀할인특약' 불러오기(import)]
from Car_insurance_logic import check_child_rider 

# [2. '테스트 케이스' 정의]
def test_자녀특약_10살_성공_케이스():
    assert check_child_rider(10) == True

def test_자녀특약_20살_실패_케이스():
    assert check_child_rider(20) == False