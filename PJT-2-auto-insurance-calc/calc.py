import time
import logging  # [New] 로깅 모듈 추가
from data import * # data.py에서 변수 가져옴

# =========================================================
# [Setup] 로깅 시스템 초기화
# =========================================================
logging.basicConfig(
    filename=LOG_CONFIG["log_file"], # calc_system.log 파일에 저장
    level=logging.INFO,              # INFO 레벨 이상만 기록
    format=LOG_CONFIG["log_format"], # 날짜/시간 포맷
    datefmt=LOG_CONFIG["date_format"],
    encoding="utf-8"                 # 한글 깨짐 방지
)

# =========================================================
# [Function Section] 핵심 산출 로직
# =========================================================

def get_standard_premium(car_type: str) -> int:
    """차종에 따른 표준(기준) 보험료 반환"""
    price = STANDARD_PREMIUMS.get(car_type, 0)
    if price == 0:
        logging.warning(f"⚠️ 존재하지 않는 차종 코드 입력됨: {car_type}")
    return price

def calculate_surcharge_rate(accidents_3yr: int, accidents_1yr: int) -> float:
    """사고 건수에 따른 할증 계수 산출"""
    rate = 1.0
    if accidents_1yr > 0:
        rate += SURCHARGE_RATES["1yr_accident"]
    if accidents_3yr > 0:
        rate += (accidents_3yr * SURCHARGE_RATES["3yr_accident"])
    return rate

def validate_age_limit(user_age: int, selected_age_code: str) -> bool:
    """운전자 연령 한정 위반 여부 검증"""
    min_age_map = {
        "AG_0000": 0, "AG_0021": 21, "AG_0026": 26, 
        "AG_0035": 35, "AG_0048": 48
    }
    required_age = min_age_map.get(selected_age_code, 0)
    
    if user_age < required_age:
        logging.info(f"⛔ 인수 거절 발생: 나이({user_age}) < 제한({required_age})")
        return False
    return True

def calculate_discount_rate(selected_specials: list) -> float:
    """선택된 특약들의 총 할인율 합산"""
    total_discount = 0.0
    for special in selected_specials:
        rate = DISCOUNT_RATES.get(special, 0.0)
        total_discount += rate
    return total_discount

def validate_conflict_specials(selected_specials: list) -> tuple:
    """[Ticket #3] 상충되는 특약(Conflict) 동시 가입 방지"""
    if "tmap" in selected_specials and "connected_car_safe" in selected_specials:
        logging.warning("⚔️ 상충 특약 선택 감지: 티맵 + 커넥티드카(안전)")
        return False, "티맵 안전운전과 커넥티드카 '안전운전' 특약은 중복해서 가입할 수 없어요."
    return True, "Pass"

def calculate_final_premium(car_type: str, user_age: int, age_code: str, acc_3yr: int, acc_1yr: int, specials: list) -> str:
    """[Final] 메인 계산 엔진 (Exception Handling 적용)"""
    try:
        # [Log] 계산 요청 기록
        logging.info(f"▶ 산출 시작 - 차종:{car_type}, 나이:{user_age}, 특약:{specials}")

        print(UX_MESSAGES["loading_start"])
        time.sleep(1)
    
        # 1. 인수 심사 (Validation)
        if not validate_age_limit(user_age, age_code):
            return f"고객{UX_MESSAGES['error_age']}"
    
        is_valid, msg = validate_conflict_specials(specials)
        if not is_valid:
            return f"{UX_MESSAGES['error_conflict']} {msg}"

        print(UX_MESSAGES["loading_calc"])
        time.sleep(1)

        # 2. 요율 산출 (Calculation)
        base = get_standard_premium(car_type)
        if base == 0:
            logging.error(f"❌ 잘못된 차종 코드 입력됨: {car_type}")
            return f"죄송해요, '{car_type}' 차량은 아직 지원하지 않아요."

        surcharge = calculate_surcharge_rate(acc_3yr, acc_1yr)
        discount = calculate_discount_rate(specials)
    
        # 3. 최종 계산
        final_rate = surcharge - discount
        final_price = int(base * final_rate)
    
        # [Log] 최종 결과 기록
        logging.info(f"✅ 산출 완료 - 최종 금액: {final_price}원")
    
        return f"{UX_MESSAGES['success']} : {format(final_price, ',')}원"

    # [사고 수습] except: "...여기서 안전하게 처리해라!"
    except Exception as e:
        # 치명적 오류(Critical)로 기록하고, 프로그램 종료 대신 안내 메시지 리턴
        logging.critical(f"🔥 시스템 치명적 오류 발생: {str(e)}")
        return "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
    
# [Test Code] 시뮬레이션 실행 
if __name__ == "__main__":
    print("\n=== 🚗 KB-Toss 자동차 보험료 산출기 (System Log On) ===\n")
    print(f"Case 1: {calculate_final_premium('grandeur', 38, 'AG_0035', 0, 0, ['blackbox', 'children'])}")
    print("\n=================================================")
    print("📢 [System] 실행 기록이 'calc_system.log' 파일에 저장되었습니다.")