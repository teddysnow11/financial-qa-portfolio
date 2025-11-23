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
# [Security Notice] 실제 요율은 대외비이므로 가상 계수(Mock Data) 사용
# ---------------------------------------------------------
SURCHARGE_RATES = {
    "1yr_accident": 0.2,  # 최근 1년 내 사고 시 20% 가중치
    "3yr_accident": 0.1   # 3년 내 사고 1건당 10% 단순 할증
}

# ---------------------------------------------------------
# 3. 운전 범위 및 연령 코드 (Driver Range & Age Codes)
# [Security Notice] 실제 코드는 대외비이므로 가상 코드(Mock Data) 사용
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

# =========================================================
# [Function Section] 핵심 산출 로직
# =========================================================

def get_standard_premium(car_type):
    """차종에 따른 표준 보험료 반환"""
    return STANDARD_PREMIUMS.get(car_type, 0)

def calculate_surcharge_rate(accidents_3yr, accidents_1yr):
    """사고 건수에 따른 할증 계수 산출 로직"""
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
    # 1. 인수 심사 (단순 리턴)
    if not validate_age_limit(user_age, age_code):
        return "인수 거절 (연령 위반)"

    # 2. 계산 로직 실행
    base = get_standard_premium(car_type)
    surcharge = calculate_surcharge_rate(acc_3yr, acc_1yr)
    discount = calculate_discount_rate(specials)
    
    final_rate = surcharge - discount
    final_price = int(base * final_rate)
    
    return final_price  