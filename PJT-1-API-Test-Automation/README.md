# PJT 1: 보험 특약 API 검증 자동화 (v1.0)

## 1. 프로젝트 목표 (Goal)
[PJT 0]에서 'Python 함수'로 '구현'했던 '자동차 특약 로직'을 '가상 API'로 '진화'시키고, Postman(수동)과 Pytest(자동)를 활용하여 'API'의 '핵심 로직'과 '예외 케이스'를 '검증'하는 것을 '목표'로 합니다.

## 2. 핵심 검증 대상 (Target)
- (v1.0) 'jsonplaceholder'를 활용한 'GET/POST' 기본 검증 (현재)
- (v2.0) [PJT 0]의 `get_rider_data()` 함수를 'GET /riders' API로 '가상 구현' 및 '검증' (예정)
- (v2.1) [PJT 0]의 `check_child_rider()` 함수를 'POST /riders/check` API로 '가상 구현' 및 '검증' (예정)

## 3. 사용 기술 (Tech Stack)
- Postman (환경 변수 활용)
- Python
- Pytest (예정)