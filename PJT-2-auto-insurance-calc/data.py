# data.py
# 데이터와 설정값(Configuration)을 관리하는 모듈

# 1. 표준 보험료 데이터 (Standard Premiums)
STANDARD_PREMIUMS = {
    "ray": 737210,      # 소형A (레이)
    "avante": 900810,   # 중형 (아반떼)
    "grandeur": 702540  # 대형 (그랜저)
}

# 2. 사고 건수별 할증 요율 (Surcharge Rates)
# [Security Notice] 실제 요율은 대외비이므로 '가상의 시뮬레이션 값' 사용
SURCHARGE_RATES = {
    "1yr_accident": 0.2,  # 1년 내 사고 가중치
    "3yr_accident": 0.1   # 3년 내 사고 건당 할증
}

# 3. 운전 범위 및 연령 코드 (Driver Range & Age Codes)
# [Security Notice] 실제 코드는 대외비이므로 '테스트용 가상 데이터(Mock Data)' 사용
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

# 4. 특약 할인율 (Discount Rates)
# [Correction] 커넥티드카 일반 할인과 '안전운전' 할인을 구분 (상충 로직용)
DISCOUNT_RATES = {
    "blackbox": 0.035,           # 블랙박스
    "children": 0.07,            # 자녀 할인
    "tmap": 0.123,               # 티맵 안전운전
    "connected_car": 0.07,       # 커넥티드카 일반
    "connected_car_safe": 0.09   # 커넥티드카 '안전운전'
}

# 5. UX 메시지 정의 (Toss Style UX Writing)
UX_MESSAGES = {
    "loading_start": "받을 수 있는 할인 특약을 한 번에 살펴볼게요", 
    "loading_calc": "보장을 바꿔서 보험료를 다시 계산할게요",
    "success": "내 최종 보험료는",
    "error_age": "님은 온라인 가입이 어려워요 (연령 한정)",
    "error_conflict": "아쉽지만"
}

# ---------------------------------------------------------
# 6. 로깅 설정 (Logging Configuration)
# [Benchmarks] Naver Logger 구조 벤치마킹 (Dev/Prod 분리)
# ---------------------------------------------------------
LOG_CONFIG = {
    "mode": "DEV",          # DEV(개발) vs PROD(운영)
    "log_file": "calc_system.log",
    "log_format": "[%(asctime)s] %(levelname)s: %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
}