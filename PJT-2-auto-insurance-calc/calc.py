import time

# ---------------------------------------------------------
# 1. 표준 보험료 데이터 (Standard Premiums)
# [Data Source] 11Z 등급 / 만 35세 이상 / 기명 1인 / 종합보험 기준
# ---------------------------------------------------------
STANDARD_PREMIUMS = {
    "ray": 737210,      # 소형A (레이)
    "avante": 900810,   # 중형 (아반떼)
    "grandeur": 702540  # 대형 (그랜저)
}

# ---------------------------------------------------------
# 2. 사고 건수별 할증 요율 (Surcharge Rates)
# ---------------------------------------------------------
# [Security Notice] 실제 보험사의 요율표는 '대외비'이므로, 로직 검증용 '가상의 시뮬레이션 값(Mock Data)' 적용
# ---------------------------------------------------------
SURCHARGE_RATES = {
    "1yr_accident": 0.2,  # (Simulation) 최근 1년 내 사고 시 20% 가중치
    "3yr_accident": 0.1   # (Simulation) 3년 내 사고 1건당 10% 단순 할증
}

# ---------------------------------------------------------
# 3. 운전 범위 및 연령 코드 (Driver Range & Age Codes)
# [Security Notice] 실제 코드는 대외비이므로 '테스트용 가상 데이터(Mock Data)' 사용
# ---------------------------------------------------------
DRIVING_RANGE_CODES = {
    "DR_0001": "기명피보험자 1인 한정",
    "DR_0002": "부부 한정",
    "DR_0003": "기명피보험자 + 자녀",
    "DR_0004": "누구나 운전"
}

AGE_LIMIT_CODES = {
    "AG_0000": "전연령 운전",
    "AG_0021": "만 21세 이상",
    "AG_0026": "만 26세 이상",
    "AG_0035": "만 35세 이상",
    "AG_0048": "만 48세 이상"
}

# ---------------------------------------------------------
# 4. 특약 할인율 (Discount Rates)
# [Public Data] 주요 특약 4가지만 선별하여 정의
# ---------------------------------------------------------
DISCOUNT_RATES = {
    "blackbox": 0.035,        # 블랙박스 (3.5%)
    "children": 0.07,         # 자녀 할인 (7%)
    "tmap": 0.123,            # 티맵 안전운전 (12.3%)
    "connected_car": 0.09     # 커넥티드카 (9%)
}

# ---------------------------------------------------------
# 5. UX 메시지 정의 (Toss Style UX Writing)
# [Refactoring] Toss 앱 화면에서 관측된 실제 문구 반영 (Evidence Based)
# ---------------------------------------------------------
UX_MESSAGES = {
    "loading_start": "받을 수 있는 할인 특약을 한 번에 살펴볼게요", 
    "loading_calc": "보장을 바꿔서 보험료를 다시 계산할게요",
    "success": "내 최종 보험료는",
    "error_age": "님은 온라인 가입이 어려워요 (연령 한정)"
}

# =========================================================
# [Function Section] 핵심 산출 로직
# =========================================================

def get_standard_premium(car_type):
    """차종에 따른 표준 보험료 반환"""
    return STANDARD_PREMIUMS.get(car_type, 0)

def calculate_surcharge_rate(accidents_3yr, accidents_1yr):
    """사고 건수에 따른 할증 계수 산출"""
    rate = 1.0
    if accidents_1yr > 0:
        rate += SURCHARGE_RATES["1yr_accident"]
    if accidents_3yr > 0:
        rate += (accidents_3yr * SURCHARGE_RATES["3yr_accident"])
    return rate

def validate_age_limit(user_age, selected_age_code):
    """운전자 연령 한정 위반 여부 검증"""
    min_age_map = {
        "AG_0000": 0, "AG_0021": 21, "AG_0026": 26, 
        "AG_0035": 35, "AG_0048": 48
    }
    required_age = min_age_map.get(selected_age_code, 0)
    if user_age < required_age:
        return False
    return True

def calculate_discount_rate(selected_specials):
    """선택된 특약들의 총 할인율 합산"""
    total_discount = 0.0
    for special in selected_specials:
        total_discount += DISCOUNT_RATES.get(special, 0.0)
    return total_discount

def calculate_final_premium(car_type, user_age, age_code, acc_3yr, acc_1yr, specials):
    """
    [Refactor] UX 메시지 적용 및 로딩 시뮬레이션 추가 (Ticket #2)
    """
    # 1. 로딩 시뮬레이션 (Toss 느낌 구현)
    print(UX_MESSAGES["loading_start"])
    time.sleep(1)  # 1초 대기

    # 2. 인수 심사 (Validation - 연령)
    if not validate_age_limit(user_age, age_code):
        # Toss 스타일: "김토스님은..." -> "고객님은..."으로 변환
        return f"고객{UX_MESSAGES['error_age']}"

    # 3. 계산 로딩 시뮬레이션
    print(UX_MESSAGES["loading_calc"])
    time.sleep(1)

    # 4. 계산 로직 실행
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
    result_1 = calculate_final_premium(
        car_type="grandeur", 
        user_age=38, 
        age_code="AG_0035", 
        acc_3yr=0, 
        acc_1yr=0, 
        specials=["blackbox", "children"]
    )
    print(f"Case 1 결과: {result_1}\n")
    
    # Case 2: 연령 위반
    result_2 = calculate_final_premium(
        car_type="avante", 
        user_age=20, 
        age_code="AG_0035", 
        acc_3yr=0, 
        acc_1yr=0, 
        specials=[]
    )
    print(f"Case 2 결과: {result_2}\n")

    print("=================================================")