import time

# ---------------------------------------------------------
# 1. 표준 보험료 데이터 (Standard Premiums)
# [Data Source] 11Z 등급 / 만 35세 이상 / 기명 1인 / 종합보험 기준 '표준 산출 보험료'
# ---------------------------------------------------------
STANDARD_PREMIUMS = {
    "ray": 737210,      # 소형A (레이)
    "avante": 900810,   # 중형 (아반떼)
    "grandeur": 702540  # 대형 (그랜저)
}

# ---------------------------------------------------------
# 2. 사고 건수별 할증 요율 (Surcharge Rates)
# ---------------------------------------------------------
# [Security Notice] 
# 실제 보험사의 요율표(등급별/차종별 상세 구간)는 '대외비'에 해당하므로,
# 본 프로젝트에서는 로직 구현을 검증하기 위한 '가상의 시뮬레이션 값(Mock Data)'을 적용했습니다.
# ---------------------------------------------------------
SURCHARGE_RATES = {
    "1yr_accident": 0.2,  # (Simulation) 최근 1년 내 사고 시 20% 가중치
    "3yr_accident": 0.1   # (Simulation) 3년 내 사고 1건당 10% 단순 할증
}

# ---------------------------------------------------------
# 3. 운전 범위 및 연령 코드 (Driver Range & Age Codes)
# [Security Notice] 실제 기간계 시스템 코드는 대외비이므로,
# 본 프로젝트에서는 로직 검증을 위한 '테스트용 가상 데이터(Mock Data)'를 사용하였습니다.
# ---------------------------------------------------------
DRIVING_RANGE_CODES = {
    "DR_0001": "기명피보험자 1인 한정",   # (Mock Data 1)
    "DR_0002": "부부 한정",             # (Mock Data 2)
    "DR_0003": "기명피보험자 + 자녀",    # (Mock Data 3)
    "DR_0004": "누구나 운전"            # (Mock Data 4)
}

AGE_LIMIT_CODES = {
    "AG_0000": "전연령 운전",           # (Mock Data: All Ages)
    "AG_0021": "만 21세 이상",          # (Mock Data: Over 21)
    "AG_0026": "만 26세 이상",          # (Mock Data: Over 26)
    "AG_0035": "만 35세 이상",          # (Mock Data: Over 35)
    "AG_0048": "만 48세 이상"           # (Mock Data: Over 48)
}

# ---------------------------------------------------------
# 4. 특약 할인율 (Discount Rates)
# [Public Data] KB손해보험 홈페이지 공시 기준 (2025.11)
# 주요 특약 4가지만 선별하여 정의하였습니다. (마일리지, 대중교통 등 생략)
# [Correction] 커넥티드카 일반 할인과 '안전운전' 할인을 구분하여 정의 (상충 로직용)
# ---------------------------------------------------------
DISCOUNT_RATES = {
    "blackbox": 0.035,           # 블랙박스 장착 (3.5%)
    "children": 0.07,            # 자녀 할인 (7%)
    "tmap": 0.123,               # 티맵 안전운전 (12.3% - 예시값)
    "connected_car": 0.07,       # 커넥티드카 일반 할인 (7%)
    "connected_car_safe": 0.09   # 커넥티드카 '안전운전' 할인 (9% - 특약 상충 대상)
}

# ---------------------------------------------------------
# 5. UX 메시지 정의 (Toss Style UX Writing)
# [Refactoring] Toss 앱 화면에서 관측된 실제 문구 반영 (Evidence Based)
# ---------------------------------------------------------
UX_MESSAGES = {
    # [Source] 할인 특약 조회 화면
    "loading_start": "받을 수 있는 할인 특약을 한 번에 살펴볼게요", 
    
    # [Source] 로딩 화면
    "loading_calc": "보장을 바꿔서 보험료를 다시 계산할게요",
    
    # [Source] 결과 화면
    "success": "내 최종 보험료는",
    
    # [Source] 가입 불가 화면 (연령 등)
    "error_age": "님은 온라인 가입이 어려워요 (연령 한정)",

    # [Source] 특약 가입 불가 화면
    "error_conflict": "아쉽지만"
}

# =========================================================
# [Function Section] 핵심 산출 로직
# =========================================================

def get_standard_premium(car_type):
    """차종에 따른 표준(기준) 보험료 반환"""
    # get(key, default) : 차종이 없으면 0원 반환 (에러 방지)
    return STANDARD_PREMIUMS.get(car_type, 0)

def calculate_surcharge_rate(accidents_3yr, accidents_1yr):
    """사고 건수에 따른 할증 계수 산출 로직
    :param accidents_3yr: 최근 3년 내 사고 건수 (int)
    :param accidents_1yr: 최근 1년 내 사고 건수 (int)
    :return: 적용될 요율 (float, 예: 1.2 = 120%)
    """
    rate = 1.0  # 기본 100%에서 시작

    # [Logic 1] 1년 내 사고가 있으면 가중치 부과
    if accidents_1yr > 0:
        rate += SURCHARGE_RATES["1yr_accident"]
    
    # [Logic 2] 3년 내 사고 건수만큼 할증 누적
    if accidents_3yr > 0:
        rate += (accidents_3yr * SURCHARGE_RATES["3yr_accident"])
        
    return rate

def validate_age_limit(user_age, selected_age_code):
    """운전자 연령 한정 위반 여부 검증
    :param user_age: 실제 운전자 나이 (int)
    :param selected_age_code: 선택한 연령 한정 코드 (str, ex:'AG_0026')
    :return: 통과(True) / 위반(False)
    """
    min_age_map = {
        "AG_0000": 0, 
        "AG_0021": 21, 
        "AG_0026": 26, 
        "AG_0035": 35, 
        "AG_0048": 48
    }
    required_age = min_age_map.get(selected_age_code, 0)
    
    if user_age < required_age:
        return False # 인수 거절
    
    return True # 인수 통과

def calculate_discount_rate(selected_specials):
    """선택된 특약들의 총 할인율 합산
    :param selected_specials: 선택된 특약 코드 리스트 (ex: ['tmap', 'blackbox'])
    :return: 총 할인율 (float, ex: 0.135)
    """
    total_discount = 0.0
    
    for special in selected_specials:
        rate = DISCOUNT_RATES.get(special, 0.0)
        total_discount += rate
        
    return total_discount

def validate_conflict_specials(selected_specials):
    """
    [Ticket #3] 상충되는 특약(Conflict) 동시 가입 방지 로직
    """
    # [Rule 1] 티맵 안전운전(tmap)과 커넥티드카 안전운전(connected_car_safe)은 중복 불가
    # (일반 커넥티드카 할인은 중복 가능함 - 도메인 지식 반영)
    if "tmap" in selected_specials and "connected_car_safe" in selected_specials:
        return False, "티맵 안전운전과 커넥티드카 '안전운전' 특약은 중복해서 가입할 수 없어요."
    
    return True, "Pass"

def calculate_final_premium(car_type, user_age, age_code, acc_3yr, acc_1yr, specials):
    """
    [Final] 티켓 1, 2, 3 모두 적용된 최종 엔진
    """
    # 1. 로딩 시뮬레이션
    print(UX_MESSAGES["loading_start"])
    time.sleep(1)  # 1초 대기 (사용자 경험 고려)
    
    # 2. 인수 심사 A (연령)
    if not validate_age_limit(user_age, age_code):
        # Toss 스타일: "고객님은..."으로 변환하여 출력
        return f"고객{UX_MESSAGES['error_age']}"
    
    # 3. 인수 심사 B (상충 특약 - Ticket #3 추가됨)
    is_valid, msg = validate_conflict_specials(specials)
    if not is_valid:
        # Toss 스타일: "아쉽지만... 중복해서 가입할 수 없어요"
        return f"{UX_MESSAGES['error_conflict']} {msg}"

    # 4. 계산 로딩
    print(UX_MESSAGES["loading_calc"])
    time.sleep(1)

    # 5. 계산 로직 실행
    base = get_standard_premium(car_type)
    surcharge = calculate_surcharge_rate(acc_3yr, acc_1yr)
    discount = calculate_discount_rate(specials)
    
    final_rate = surcharge - discount
    final_price = int(base * final_rate)
    
    return f"{UX_MESSAGES['success']} : {format(final_price, ',')}원"

# [Test Code] 시뮬레이션 실행
if __name__ == "__main__":
    print("\n=== 🚗 KB-Toss 자동차 보험료 산출기 (Logic & UX Integration) ===\n")
    
    # Case 1: 정상 가입 (그랜저, 38세, 무사고, 블랙박스+자녀 할인)
    print(f"Case 1: {calculate_final_premium('grandeur', 38, 'AG_0035', 0, 0, ['blackbox', 'children'])}")
    print("-" * 30)

    # Case 2: 연령 위반 (20세가 35세 특약 가입)
    print(f"Case 2: {calculate_final_premium('avante', 20, 'AG_0035', 0, 0, [])}")
    print("-" * 30)

    # Case 3: 상충 특약 동시 선택 (티맵 + 커넥티드카안전운전 -> 거절되어야 함!)
    # 주의: 일반 커넥티드카 할인이 아니라 'safe' 버전을 넣어야 충돌남
    print(f"Case 3: {calculate_final_premium('ray', 30, 'AG_0026', 0, 0, ['tmap', 'connected_car_safe'])}")
    
    print("\n=================================================")