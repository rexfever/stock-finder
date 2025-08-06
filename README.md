# 키움증권 주식 검색기

키움증권 REST API를 활용한 웹 기반 주식 조건검색 시스템입니다.

## ✨ 주요 기능

- 🔍 **조건검색**: 키움 HTS에서 저장한 조건검색식 실행
- 📊 **기술지표 분석**: TEMA, DEMA, MACD, RSI, OBV 자동 계산
- 💡 **매매전략**: 조건 충족 종목에 대한 전략 및 신뢰도 제공
- 📈 **실시간 현재가**: 검색된 종목의 최신 가격 정보
- 🎯 **필터링**: 골든크로스 등 엄격한 조건으로 종목 선별

## 🚀 검색 조건

시스템은 다음 조건을 모두 만족하는 종목을 찾습니다:

1. **골든크로스**: TEMA(20) > DEMA(10) AND TEMA(20)[전일] < DEMA(10)[전일]
2. **MACD**: MACD Oscillator(12,26,9) > -50
3. **RSI**: RSI(14) > 55
4. **거래량**: 당일 거래량 > 평균거래량(5일) × 1.5

## 📁 프로젝트 구조

```
workspace/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 API 서버
│   ├── start.py            # 서버 시작 스크립트
│   ├── kiwoom_auth.py      # 키움 OAuth 인증
│   ├── kiwoom_service.py   # 키움 API 서비스
│   ├── condition_service.py # 조건 검증 및 기술지표
│   ├── stock_models.py     # 데이터 모델
│   ├── requirements.txt    # Python 의존성
│   ├── .env.example        # 환경변수 예제
│   └── .env               # 환경변수 (직접 생성)
└── frontend/               # React 프론트엔드
    ├── public/
    ├── src/
    │   ├── components/     # React 컴포넌트
    │   ├── services/       # API 통신
    │   └── utils/          # 유틸리티
    ├── package.json
    └── tailwind.config.js
```

## 🔧 설치 및 실행

### 1. 환경 설정

#### 키움증권 API 준비
1. [키움증권 OpenAPI](https://www.kiwoom.com/h/customer/download/VOpenApiInfoView?dummyVal=0) 가입
2. 앱 키(App Key)와 앱 시크릿(App Secret) 발급

#### 조건검색식 저장
1. 키움 HTS 실행
2. **[0150] 조건검색** 메뉴 이동
3. 새 조건검색식 생성 후 **"사용자_조건검색식"** 이름으로 저장
   - 또는 원하는 이름으로 저장 (실행 시 해당 이름 입력)

### 2. 백엔드 설정

```bash
# 백엔드 디렉터리로 이동
cd backend

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
```

#### `.env` 파일 설정
```env
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_APP_SECRET=your_app_secret_here
```

### 3. 프론트엔드 설정

```bash
# 프론트엔드 디렉터리로 이동
cd frontend

# 의존성 설치
npm install
```

### 4. 실행

#### 백엔드 서버 시작
```bash
cd backend
python start.py
# 또는
uvicorn main:app --reload
```

#### 프론트엔드 서버 시작
```bash
cd frontend
npm start
```

### 5. 접속

- **웹 애플리케이션**: http://localhost:3000
- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/health

## 📊 API 엔드포인트

### 주요 API

| 메서드 | 엔드포인트 | 설명 |
|--------|------------|------|
| GET | `/health` | 서버 상태 확인 |
| POST | `/api/search?condition_name=조건명` | 조건검색 실행 |
| GET | `/api/conditions` | 사용 가능한 조건검색식 목록 |

### 응답 예시

```json
{
  "success": true,
  "message": "검색 완료: 5개 종목 분석",
  "stocks": [
    {
      "stock_info": {
        "code": "005930",
        "name": "삼성전자",
        "price": 71000,
        "change_percent": 2.3,
        "volume": 12500000
      },
      "indicators": {
        "tema_20": 71200,
        "dema_10": 70800,
        "macd_oscillator": 120.5,
        "rsi_14": 62.3,
        "volume_ratio": 1.8
      },
      "strategy": {
        "signal": "BUY",
        "description": "강력한 상승 신호 - 적극 매수 고려",
        "confidence": 0.85
      },
      "meets_conditions": true
    }
  ],
  "total_count": 5,
  "search_time": "2024-01-15T10:30:00"
}
```

## 🔧 기술지표 설명

### TEMA (Triple Exponential Moving Average)
- 삼중 지수이동평균으로 가격 변화에 빠르게 반응
- 단기 추세 파악에 효과적

### DEMA (Double Exponential Moving Average)  
- 이중 지수이동평균으로 지연(lag) 감소
- 추세 전환점 조기 감지

### MACD (Moving Average Convergence Divergence)
- 12일/26일 EMA 차이로 모멘텀 측정
- Oscillator > -50 조건으로 상승 모멘텀 확인

### RSI (Relative Strength Index)
- 0~100 범위의 모멘텀 지표
- 55 초과 시 상승 추세 신호

### OBV (On-Balance Volume)
- 거래량과 가격 변화의 상관관계 분석
- 추세 지속성 판단에 활용

## 🚨 트러블슈팅

### 일반적인 문제

#### 1. 인증 실패
```
Error: 키움 API 인증이 필요합니다
```
**해결방법**: 
- `.env` 파일의 API 키 확인
- 키움증권 OpenAPI 포털에서 키 상태 확인

#### 2. 조건검색식 오류
```
Error: 조건검색식을 찾을 수 없습니다
```
**해결방법**:
- 키움 HTS에서 조건검색식 저장 여부 확인
- 정확한 조건검색식 이름 입력

#### 3. CORS 에러
```
Access to fetch at 'http://localhost:8000' blocked by CORS policy
```
**해결방법**:
- 백엔드 서버가 정상 실행 중인지 확인
- 포트 번호 확인 (백엔드: 8000, 프론트엔드: 3000)

#### 4. 타임아웃 에러
```
Error: timeout of 30000ms exceeded
```
**해결방법**:
- 네트워크 연결 상태 확인
- 키움 API 서버 상태 확인
- 조건검색 결과가 너무 많은 경우 조건 세분화

### 로그 확인

#### 백엔드 로그
```bash
cd backend
python start.py
# 콘솔에서 API 호출 및 에러 로그 확인
```

#### 프론트엔드 로그
- 브라우저 개발자 도구 → Console 탭에서 확인

## 📈 개발 정보

### 기술 스택

**백엔드**:
- FastAPI 0.104.1
- Python 3.8+
- Pandas (기술지표 계산)
- Requests (HTTP 통신)

**프론트엔드**:
- React 18.2.0
- Tailwind CSS 3.3.6
- Axios (API 통신)

### 개발 모드 실행

```bash
# 백엔드 개발 모드 (자동 재시작)
cd backend
uvicorn main:app --reload

# 프론트엔드 개발 모드 (자동 재시작)
cd frontend  
npm start
```

## ⚠️ 주의사항

1. **투자 판단**: 본 시스템은 정보 제공 목적이며, 투자 결정은 사용자 책임입니다.
2. **API 제한**: 키움 API 호출 횟수 제한을 고려하여 사용하세요.
3. **실시간 데이터**: 지연될 수 있으며, 실제 거래 시 최신 정보를 확인하세요.
4. **백테스팅**: 과거 데이터 기반이므로 미래 수익을 보장하지 않습니다.

## 📞 지원

문제 발생 시:
1. 이 README의 트러블슈팅 섹션 확인
2. API 문서 (http://localhost:8000/docs) 참조
3. 키움증권 OpenAPI 고객센터 문의

---

**면책조항**: 이 소프트웨어는 교육 및 정보 제공 목적으로 제작되었습니다. 실제 투자 결정에 대한 책임은 사용자에게 있으며, 개발자는 투자 손실에 대해 책임지지 않습니다.