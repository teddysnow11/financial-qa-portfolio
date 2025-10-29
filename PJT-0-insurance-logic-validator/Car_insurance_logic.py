# [PJT 0 - v1.0] 자동차보험 할인특약 데이터 구조 (List of Dicts)
# - v1.0: 3대 특약(마일리지, 자녀, 블랙박스) 정의
# - v1.0: (Fix) 치명적인 SyntaxError (콤마, 콜론 등) 9곳 수정



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
] # <-- 자동차 보험 할인특약 v1.0 데이터 (자료) 끝
# ==============================================
# [PJT 0 - v1.1] 데이터 '활용' (완성본)
# - v1.1: (Logic) 'for'문을 사용해 '자료'를 '출력'
# ==============================================

print("== [PJT 0] 자동차 특약 리스트 (v1.1) ==")
print(f"총 {len(car_special_clause)}개의 특약이 등록되어 있습니다.") # 'len()'으로 총 개수 세기
print("-" * 40)

# 'car_special_clause'라는 '리스트(List)'를 'for'문으로 '출력' 시작
for rider in car_special_clause:
    # 'rider'는 딕셔너리(Dict) 1개입니다.
    print(f"특약명: {rider['special_clause_name']}")
    print(f"조건: {rider['condition']}")
    print(f"필요 자료: {rider['required_evidence']}")
    print(f"최대 할인율: {rider['max_discount_rate']}%") # '데이터'엔 숫자만, '출력'할 때 '%' 붙이기!
    print("-" * 40)
