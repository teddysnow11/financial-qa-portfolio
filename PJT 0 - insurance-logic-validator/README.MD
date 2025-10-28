# [PJT 0] 자동차보험 할인특약 (List of Dicts 구조)
Car special clause = [
    {
        'special_clause_name': '마일리지 할인',
        'condition': '연 15,000km 이하 주행',
        'required_docs': ['최초 계기판사진'],
        'max_discount_rate': 37
    },
    {
        'special_clause_name': '자녀 할인',
        'condition': '만 13세 이하 자녀',
        'required_docs': ['가족관계증명서','등본','임신확인서'],
        'max_discount_rate': 13
    },
    {
        'special_clause_name': '블랙박스 할인',
        'condition': ['블랙박스 장착 차량','빌트인캠 장착 차량']
        'required_docs': ['블랙박스 사진','빌트인캠 장착정보'],
        'max_discount_rate': 10
    }
]