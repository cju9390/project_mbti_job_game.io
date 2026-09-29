# MBTI × RPG 판타지 직업 예측 웹앱

60문항 MBTI 설문을 XGBoost로 분석해 성격 유형을 예측하고, 판타지 RPG 직업·6가지 스탯·보완형 파티를 추천하는 Flask 웹앱입니다.

- **소개 페이지 (GitHub Pages)**: https://cju9390.github.io/project_mbti_job_game.io/
- **포트폴리오**: [Notion 상세 페이지](https://www.notion.so/Portfolio-AI-356a28e78b6f818f96d1c1e040fbdc38)

| 항목 | 내용 |
|---|---|
| 형태 | 개인 프로젝트 (기획·개발·배포 전담) |
| 데이터 | [60k Responses of 16 Personalities Test (Kaggle)](https://www.kaggle.com/datasets/anshulmehtakaggl/60k-responses-of-16-personalities-test-mbt) |
| 스택 | Python, Flask, XGBoost, SQLite3, Chart.js |

## 동작 방식

```
60문항 설문 → Flask → XGBoost 축별 이진 분류기 4개 (EI/NS/TF/JP)
  → 축별 확률로 6가지 RPG 스탯 계산 (무력·마력·신성력·민첩성·통솔력·생존력)
  → MBTI별 직업 매핑 (16종) → SQLite 저장
  → 결과 페이지: Chart.js 레이더 차트 + 파티 추천
```

- **스탯 공식** — 예: 무력 = (P(S) + P(T)) / 2 × 9 + 1, 직업 보너스 적용 후 최대 10으로 제한
- **보완형 파티 추천** — 사용자의 가장 낮은 스탯 3개를 찾아 DB에서 해당 스탯이 가장 높은 모험가를 선발 (직업 중복 제외)
- **퀘스트별 추천** — 토벌·수호·마법탐구·외교·생존 5가지 유형별 우선 스탯 순서로 파티 구성

## 해결한 버그 — ISTJ 편향

대부분의 사용자가 ISTJ로 분류되는 현상이 있었습니다. 원인은 문항별 방향성(`QUESTION_DIRECTIONS`)이 적용되지 않아 일부 문항의 점수 방향이 반전되지 않은 것이었고, 방향성 배열을 적용해 축별 점수를 정규화해 해결했습니다.

## 코드

```
index.html              소개 페이지 (GitHub Pages)
app/
  app.py                Flask 서버 (/, /register, /result, /api/party-members)
  mbti_preprocessing.py 원본 7점 척도 → -1~1 스케일 변환
  train_models.py       축별 XGBoost 학습 → models.pkl
  seed_db.py            SQLite 초기화 + NPC 16명 시드 데이터
```

> `app/model.py`(예측·스탯 변환 로직)와 `templates/`(intro·index·result.html)는 아직 업로드 전입니다.

## 실행

```bash
cd app
pip install flask xgboost scikit-learn pandas numpy qrcode
python mbti_preprocessing.py   # 16P.csv 필요 (Kaggle)
python train_models.py
python seed_db.py
python app.py                  # http://0.0.0.0:8080, 같은 Wi-Fi 접속용 QR 코드 생성
```
