# [PJT 0.5 - v2.0] '2차원 매트릭스' 구조 (Nested Dict)
# - v2.0: 15년 경력의 '사고 건수별 요율표'를 '데이터화'

CAR_NUMBER_OF_CLAIMS_RATES = {
    # '3년 사고건수': '0'
    '0': { 
        '0': -15.0 # '1년 사고건수(0)' -> 15% 할인
    },
    # '3년 사고건수': '1'
    '1': { 
        '0': -3.0, # '1년 사고건수(0)' -> 3% 할인
        '1': 5.0   # '1년 사고건수(1)' -> 5% 할증
    },
    # '3년 사고건수': '2'
    '2': {
        '0': -3.0,
        '1': 7.0,
        '2': 10.0
    },
    # '3년 사고건수': '3+' (3건 이상)
    '3+': {
        '0': -3.0,
        '1': 5.0,
        '2': 15.0,
        '3+': 20.0
    }
}

# [PJT 0.5 - v2.0] '요리법(함수)': '2차원 매트릭스'를 '조회'하는 함수
def find_accident_loading_rate(acc_3yr, acc_1yr):
    
    # --- 1. '3년 사고 건수'를 'Key'로 '번역' ---
    if acc_3yr == 0:
        key_3yr = '0'
    elif acc_3yr == 1:
        key_3yr = '1'
    elif acc_3yr == 2:
        key_3yr = '2'
    else: # 3건 이상
        key_3yr = '3+'

    # --- 2. '1년 사고 건수'를 'Key'로 '번역' ---
    if acc_1yr == 0:
        key_1yr = '0'
    elif acc_1yr == 1:
        key_1yr = '1'
    elif acc_1yr == 2:
        key_1yr = '2'
    else: # 3건 이상
        key_1yr = '3+'
        
    # --- 3. '데이터'에서 '값'을 '조회(Lookup)' ---
    
    try:
        # 1단계: 3년 사고 'Key'로 '내부 딕셔너리'를 찾음
        rate_table_1yr = CAR_NUMBER_OF_CLAIMS_RATES[key_3yr]
        
        # 2단계: 1년 사고 'Key'로 '최종 요율'을 찾음
        rate = rate_table_1yr[key_1yr]

        return rate
        
    except KeyError:
        print(f"[경고] 정의되지 않은 규칙입니다! (3년: {acc_3yr}건, 1년: {acc_1yr}건)")
        return None # 'None' (결과 없음)을 '반환'
        
# ===============================================
# [PJT 0.5 - v2.0] 검증(Test): 테스트케이스
# ===============================================

print("== [PJT 0.5] 2차원 '사고 할증 요율' 체화 훈련 ==")

# T/C 1: (3년 2건, 1년 1건) -> 7.0% 예상
# '함수'를 '호출(Call)'하고 '결과(print)'를 '검증'합니다.
print(f"3년 2건, 1년 1건: {find_accident_loading_rate(2, 1)}"+"%")

# T/C 2: (3년 5건, 1년 10건) -> '3+','3+' -> 20.0% 예상
print(f"3년 5건, 1년 10건: {find_accident_loading_rate(5, 10)}"+"%")

# T/C 3: (3년 0건, 1년 0건) -> -15.0% 예상
print(f"3년 0건, 1년 0건: {find_accident_loading_rate(0, 0)}"+"%")

# T/C 4: (Gap) (3년 0건, 1년 1건) -> 'None' 및 '[경고]' 메시지 예상
print(f"3년 0건, 1년 1건: {find_accident_loading_rate(0, 1)}")