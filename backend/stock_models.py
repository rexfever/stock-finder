from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StockInfo(BaseModel):
    """종목 기본 정보"""
    code: str
    name: str
    price: float
    change_percent: float
    volume: int


class TechnicalIndicators(BaseModel):
    """기술 지표"""
    tema_20: float
    dema_10: float
    macd_oscillator: float
    rsi_14: float
    obv: float
    avg_volume_5: float
    volume_ratio: float


class TradingStrategy(BaseModel):
    """매매 전략"""
    signal: str  # "BUY", "SELL", "HOLD"
    description: str
    confidence: float  # 0.0 ~ 1.0


class AnalyzedStock(BaseModel):
    """분석된 종목 정보"""
    stock_info: StockInfo
    indicators: TechnicalIndicators
    strategy: TradingStrategy
    meets_conditions: bool


class StockSearchResponse(BaseModel):
    """검색 응답"""
    success: bool
    message: str
    stocks: List[AnalyzedStock]
    total_count: int
    search_time: datetime