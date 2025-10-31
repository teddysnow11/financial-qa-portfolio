# [PJT 0 - v1.2] '함수(Function)'로 '진화'
# - v1.2: '데이터'와 '출력 로직'을 '함수'로 '분리'
# - v1.2: (Feat) '15년 경력'을 담은 '첫 번째 로직 함수(check_child_rider)' 구현

# [실행 1: '데이터 함수' (데이터 정의)]
def get_rider_data():
    car_special_clause = [
        {
            'special_clause_name': '마일리지 할인 특약',
            'condition': '연 15,000km 이하 주행',
            'required_evidence': ['최초 계기판사진' , '커넥티드카 주행거리정보'],
            'max_discount_rate': 35.3
        },
        {
            'special_clause_name': '자녀 할인 특약',
            'condition': '만 13세 이하 자녀',
            'required_evidence': ['가족관계증명서' , '등본' , '임신확인서'],
            'max_discount_rate': 15.3
        },
        {
            'special_clause_name': '블랙박스 할인 특약',
            'condition': ['블랙박스 장착차량' , '빌트인캠 장착차량'],
            'required_evidence': ['블랙박스 사진' , '빌트인캠 장착정보'],
            'max_discount_rate': 7
        }
    ]
    return car_special_clause

# [실행 2: '출력 함수' (데이터 활용)]
def print_all_riders(rider_list):
    print("== [PJT 0] 자동차 특약 리스트 (v1.2) ==")
    print(f"총 {len(rider_list)}개의 특약이 등록되어 있습니다.")
    print("-" * 40)
    for rider in rider_list:
        print(f"특약명: {rider['special_clause_name']}")
        print(f"조건: {rider['condition']}")
        print(f"필요 자료: {rider['required_evidence']}")
        print(f"최대 할인율: {rider['max_discount_rate']}%")
        print("-" * 40)

# ===============================================
# [실행 3: '로직 함수' (⭐오늘의 핵심⭐)
# - v1.2: (Logic) '자녀 할인 특약'의 '조건(나이)'을 '검증'하는 함수
# ===============================================
def check_child_rider(customer_age):
    if customer_age <= 13:
        print(f"[검증 결과] 나이: {customer_age}세 -> 자녀 할인 '대상'입니다.")
        return True  # '대상'이라는 '결과'를 '반환'
    else:
        print(f"[검증 결과] 나이: {customer_age}세 -> 자녀 할인 '비대상'입니다.")
        return False # '비대상'이라는 '결과'를 '반환'

# ===============================================
# [실행 4: '메인(Main) 영역']
# ===============================================

# 1. '데이터 함수'를 '호출'해서 '재료'를 가져옵니다.
all_riders_data = get_rider_data()

# 2. '출력 함수'에 '재료'를 '전달'해서 '실행'시킵니다.
print_all_riders(all_riders_data)

# 3. '로직 함수'를 '테스트'합니다.
print("\n== [PJT 0] 자녀 특약 조건 검증 테스트 (v1.2) ==")
check_child_rider(10) # T/C 1: 10살 테스트
check_child_rider(20) # T/C 2: 20살 테스트