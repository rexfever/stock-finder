from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
import asyncio
import logging

from stock_models import StockSearchResponse, AnalyzedStock, StockInfo
from kiwoom_service import KiwoomService
from condition_service import ConditionService

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="키움증권 주식 검색기 API",
    description="키움증권 REST API를 활용한 주식 조건검색 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 인스턴스
kiwoom_service = KiwoomService()
condition_service = ConditionService()


@app.get("/")
async def root():
    """API 상태 확인"""
    return {"message": "키움증권 주식 검색기 API", "status": "running"}


@app.get("/health")
async def health_check():
    """헬스체크"""
    try:
        # 키움 인증 테스트
        token = kiwoom_service.auth.get_access_token()
        return {"status": "healthy", "auth": "ok" if token else "fail"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/api/search", response_model=StockSearchResponse)
async def search_stocks(condition_name: str):
    """조건검색식을 사용한 종목 검색"""
    start_time = datetime.now()
    
    try:
        logger.info(f"조건검색 시작: {condition_name}")
        
        # 1. 조건검색으로 종목 코드 리스트 가져오기
        stock_codes = kiwoom_service.search_by_condition(condition_name)
        logger.info(f"조건검색 결과: {len(stock_codes)}개 종목")
        
        if not stock_codes:
            return StockSearchResponse(
                success=True,
                message="조건에 맞는 종목이 없습니다.",
                stocks=[],
                total_count=0,
                search_time=datetime.now()
            )
        
        # 2. 각 종목에 대해 상세 분석 수행
        analyzed_stocks = []
        
        for stock_code in stock_codes[:20]:  # 최대 20개 종목만 분석
            try:
                # 종목 기본 정보 조회
                price_info = kiwoom_service.get_stock_price(stock_code)
                stock_name = kiwoom_service.get_stock_name(stock_code)
                
                # 차트 데이터 조회 (30일)
                chart_data = kiwoom_service.get_stock_chart_data(stock_code, period="D", count=30)
                
                if not chart_data:
                    continue
                
                # 기술지표 계산
                indicators = condition_service.calculate_indicators(chart_data)
                
                # 조건 검증
                meets_conditions = condition_service.meets_all_conditions(indicators, chart_data)
                
                # 매매 전략 생성
                strategy = condition_service.generate_trading_strategy(indicators, meets_conditions)
                
                # 종목 정보 구성
                stock_info = StockInfo(
                    code=stock_code,
                    name=stock_name,
                    price=price_info["price"],
                    change_percent=price_info["change_percent"],
                    volume=price_info["volume"]
                )
                
                analyzed_stock = AnalyzedStock(
                    stock_info=stock_info,
                    indicators=indicators,
                    strategy=strategy,
                    meets_conditions=meets_conditions
                )
                
                analyzed_stocks.append(analyzed_stock)
                logger.info(f"분석 완료: {stock_name} ({stock_code})")
                
            except Exception as e:
                logger.error(f"종목 분석 실패 {stock_code}: {str(e)}")
                continue
        
        # 조건 충족하는 종목만 필터링 (선택사항)
        # analyzed_stocks = [stock for stock in analyzed_stocks if stock.meets_conditions]
        
        # 신뢰도 순으로 정렬
        analyzed_stocks.sort(key=lambda x: x.strategy.confidence, reverse=True)
        
        search_time = datetime.now()
        duration = (search_time - start_time).total_seconds()
        
        logger.info(f"검색 완료: {len(analyzed_stocks)}개 종목, {duration:.2f}초 소요")
        
        return StockSearchResponse(
            success=True,
            message=f"검색 완료: {len(analyzed_stocks)}개 종목 분석",
            stocks=analyzed_stocks,
            total_count=len(analyzed_stocks),
            search_time=search_time
        )
        
    except Exception as e:
        logger.error(f"검색 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"검색 중 오류가 발생했습니다: {str(e)}")


@app.get("/api/conditions")
async def get_available_conditions():
    """사용 가능한 조건검색식 목록 (더미 데이터)"""
    return {
        "conditions": [
            "사용자_조건검색식",
            "골든크로스_상승",
            "기술적_반등_신호"
        ],
        "message": "키움 HTS에서 저장한 조건검색식 이름을 사용하세요"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)