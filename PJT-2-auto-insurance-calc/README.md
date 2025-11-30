# 🚗 Auto Insurance Calculator (자동차 보험료 산출기)

### 📋 프로젝트 소개
KB손해보험의 **'정교한 도메인 로직(안정성)'**과 Toss의 **'사용자 친화적 UX(속도)'**를 결합하여, 실제 보험료 산출 과정을 시뮬레이션한 Python 프로젝트입니다.

### 🎯 핵심 구현 목표 (Key Features)
1.  **핵심 산출 로직 (Logic):** '11Z 등급' 실데이터 및 사고 건수(3년/1년) 기반 할증 계수 적용
2.  **상충 특약 방어 (Risk Management):** '티맵' vs '커넥티드카 안전운전' 등 중복 가입 불가 케이스에 대한 방어 로직(Validation) 구현
3.  **UX Writing 개선 (Refactoring):** 딱딱한 금융 용어를 사용자 중심의 언어(Toss Style)로 재설계

### 🛠 기술 스택 (Tech Stack)
- **Language:** Python 3.x
- **Cooperation:** Git Flow (Feature/Fix/Refactor), Issue Tracking

## 🚀 Technical Challenge: 레거시(Legacy)와 모던(Modern) 시스템 데이터 정합성 검증

**[Issue] 레거시(Legacy)와 모던(Modern) 시스템 간 데이터 불일치**
- **상황:** REST API(JSON) 기반의 채널계(Toss)와 WebSquare(XML) 기반의 기간계(KB) 간 데이터 통신 시, **데이터 타입 불일치** 및 **필드 매핑 누락** 리스크를 발견했습니다.
- **분석:** 실제 네트워크 패킷(Payload)을 분석하여, 양쪽 시스템의 변수명(`joinMall` vs `conn_id`) 매핑 테이블을 도출했습니다.  

**[Solution] Pytest를 활용한 아키텍처 검증**
- **해결:** `Pytest`를 활용하여 Toss의 JSON 데이터가 KB의 XML 전문 규격(예: `apcno`는 'RQ'로 시작)을 준수하는지 검증하는 **자동화 테스트 시나리오**를 구현했습니다. (`test_json_to_xml_mapping_verification`)

## 💡 Business & UX Strategy: 금융권과 핀테크의 간극 해결

**1. UX Writing (Toss Style)**
* **As-Is (기존 금융):** "연령 한정 특약 위반으로 가입 불가합니다." (딱딱함, 통보식)
* **To-Be (개선안):** "고객님은 연령 한정 특약 때문에 가입이 어려워요." (대화형, 거부감 완화)
* **적용:** `data.py`의 `UX_MESSAGES`에 토스의 톤앤매너를 반영하여 **고객 이탈률(Bounce Rate) 방어 설계**.

**2. Legacy System Latency (KB Style)**
* **분석:** 구형 기간계 시스템(WebSquare)은 로직 처리에 물리적 시간이 소요됨을 확인.
* **적용:** `calc.py`에 `time.sleep(1)`을 의도적으로 삽입하여, 실제 금융권 연동 시 발생하는 **'로딩 지연(Latency)'** 상황을 시뮬레이션하고 사용자에게 **안내 문구를 노출**함.