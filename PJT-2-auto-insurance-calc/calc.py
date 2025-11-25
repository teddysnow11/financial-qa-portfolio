import time
from data import * # [Module] 데이터 파일(data.py)에서 모든 변수를 가져옴

# =========================================================
# [Function Section] 핵심 산출 로직
# =========================================================

def get_standard_premium(car_type: str) -> int:
    """차종에 따른 표준(기준) 보험료 반환"""
    return STANDARD_PREMIUMS.get(car_type, 0)

def calculate_surcharge_rate(accidents_3yr: int, accidents_1yr: int) -> float:    """사고 건수에 따른 할증 계수 산출 로직"""
    rate = 1.0
    if accidents_1yr > 0:
        rate += SURCHARGE_RATES["1yr_accident"]
    if accidents_3yr > 0:
        rate += (accidents_3yr * SURCHARGE_RATES["3yr_accident"])
    return rate

def validate_age_limit(user_age: int, selected_age_code: str) -> bool:    """운전자 연령 한정 위반 여부 검증"""
    min_age_map = {
        "AG_0000": 0, "AG_0021": 21, "AG_0026": 26, 
        "AG_0035": 35, "AG_0048": 48
    }
    required_age = min_age_map.get(selected_age_code, 0)
    if user_age < required_age:
        return False
    return True

def calculdef calculate_discount_rate(selected_specials: list) -> float:ate_discount_rate(selected_specials):
    """선택된 특약들의 총 할인율 합산"""
    total_discount = 0.0
    for special in selected_specials:
        rate = DISCOUNT_RATES.get(special, 0.0)
        total_discount += rate
    return total_discount

def validate_conflict_specials(selected_specials: list) -> tuple:    """[Ticket #3] 상충되는 특약(Conflict) 동시 가입 방지 로직"""
    if "tmap" in selected_specials and "connected_car_safe" in selected_specials:
        return False, "티맵 안전운전과 커넥티드카 '안전운전' 특약은 중복해서 가입할 수 없어요."
    return True, "Pass"

def calculate_final_premium(car_type: str, user_age: int, age_code: str, acc_3yr: int, acc_1yr: int, specials: list) -> str:    """[Final] 메인 계산 엔진"""
    print(UX_MESSAGES["loading_start"])
    time.sleep(1)
    
    if not validate_age_limit(user_age, age_code):
        return f"고객{UX_MESSAGES['error_age']}"
    
    is_valid, msg = validate_conflict_specials(specials)
    if not is_valid:
        return f"{UX_MESSAGES['error_conflict']} {msg}"

    print(UX_MESSAGES["loading_calc"])
    time.sleep(1)

    base = get_standard_premium(car_type)
    surcharge = calculate_surcharge_rate(acc_3yr, acc_1yr)
    discount = calculate_discount_rate(specials)
    
    final_rate = surcharge - discount
    final_price = int(base * final_rate)
    
    return f"{UX_MESSAGES['success']} : {format(final_price, ',')}원"

# [Test Code] 시뮬레이션 실행
if __name__ == "__main__":
    print("\n=== 🚗 KB-Toss 자동차 보험료 산출기 (Logic & UX Integration) ===\n")
    
    # Case 1: 정상 가입
    print(f"Case 1: {calculate_final_premium('grandeur', 38, 'AG_0035', 0, 0, ['blackbox', 'children'])}")
    print("-" * 30)
    # Case 2: 연령 위반
    print(f"Case 2: {calculate_final_premium('avante', 20, 'AG_0035', 0, 0, [])}")
    print("-" * 30)
    # Case 3: 상충 특약
    print(f"Case 3: {calculate_final_premium('ray', 30, 'AG_0026', 0, 0, ['tmap', 'connected_car_safe'])}")
    print("\n=================================================")