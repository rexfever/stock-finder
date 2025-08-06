import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from stock_models import TechnicalIndicators, TradingStrategy


class ConditionService:
    """조건 검증 및 기술지표 계산 서비스"""
    
    @staticmethod
    def calculate_tema(prices: List[float], period: int) -> float:
        """TEMA (Triple Exponential Moving Average) 계산"""
        if len(prices) < period:
            return 0.0
        
        series = pd.Series(prices)
        ema1 = series.ewm(span=period).mean()
        ema2 = ema1.ewm(span=period).mean()
        ema3 = ema2.ewm(span=period).mean()
        
        tema = 3 * ema1 - 3 * ema2 + ema3
        return float(tema.iloc[-1])
    
    @staticmethod
    def calculate_dema(prices: List[float], period: int) -> float:
        """DEMA (Double Exponential Moving Average) 계산"""
        if len(prices) < period:
            return 0.0
        
        series = pd.Series(prices)
        ema1 = series.ewm(span=period).mean()
        ema2 = ema1.ewm(span=period).mean()
        
        dema = 2 * ema1 - ema2
        return float(dema.iloc[-1])
    
    @staticmethod
    def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
        """MACD 계산 (MACD Line, Signal Line, Oscillator)"""
        if len(prices) < slow:
            return 0.0, 0.0, 0.0
        
        series = pd.Series(prices)
        ema_fast = series.ewm(span=fast).mean()
        ema_slow = series.ewm(span=slow).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        oscillator = macd_line - signal_line
        
        return float(macd_line.iloc[-1]), float(signal_line.iloc[-1]), float(oscillator.iloc[-1])
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """RSI (Relative Strength Index) 계산"""
        if len(prices) < period + 1:
            return 50.0
        
        series = pd.Series(prices)
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1])
    
    @staticmethod
    def calculate_obv(prices: List[float], volumes: List[int]) -> float:
        """OBV (On-Balance Volume) 계산"""
        if len(prices) != len(volumes) or len(prices) < 2:
            return 0.0
        
        obv = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                obv += volumes[i]
            elif prices[i] < prices[i-1]:
                obv -= volumes[i]
        
        return float(obv)
    
    @staticmethod
    def calculate_average_volume(volumes: List[int], period: int = 5) -> float:
        """평균 거래량 계산"""
        if len(volumes) < period:
            return float(np.mean(volumes)) if volumes else 0.0
        
        return float(np.mean(volumes[-period:]))
    
    def calculate_indicators(self, chart_data: List[Dict[str, Any]]) -> TechnicalIndicators:
        """모든 기술지표 계산"""
        if not chart_data:
            return TechnicalIndicators(
                tema_20=0, dema_10=0, macd_oscillator=0,
                rsi_14=50, obv=0, avg_volume_5=0, volume_ratio=1.0
            )
        
        # 데이터 추출
        prices = [item["close"] for item in chart_data]
        volumes = [item["volume"] for item in chart_data]
        
        # 기술지표 계산
        tema_20 = self.calculate_tema(prices, 20)
        dema_10 = self.calculate_dema(prices, 10)
        _, _, macd_oscillator = self.calculate_macd(prices)
        rsi_14 = self.calculate_rsi(prices)
        obv = self.calculate_obv(prices, volumes)
        avg_volume_5 = self.calculate_average_volume(volumes, 5)
        
        # 거래량 비율
        current_volume = volumes[-1] if volumes else 0
        volume_ratio = current_volume / avg_volume_5 if avg_volume_5 > 0 else 1.0
        
        return TechnicalIndicators(
            tema_20=tema_20,
            dema_10=dema_10,
            macd_oscillator=macd_oscillator,
            rsi_14=rsi_14,
            obv=obv,
            avg_volume_5=avg_volume_5,
            volume_ratio=volume_ratio
        )
    
    def check_golden_cross_condition(self, chart_data: List[Dict[str, Any]]) -> bool:
        """골든크로스 조건 확인: TEMA(20) > DEMA(10) AND TEMA(20)[1] < DEMA(10)[1]"""
        if len(chart_data) < 21:  # 최소 21일 데이터 필요
            return False
        
        # 현재 값들
        current_prices = [item["close"] for item in chart_data]
        current_tema = self.calculate_tema(current_prices, 20)
        current_dema = self.calculate_dema(current_prices, 10)
        
        # 전일 값들
        prev_prices = [item["close"] for item in chart_data[:-1]]
        prev_tema = self.calculate_tema(prev_prices, 20)
        prev_dema = self.calculate_dema(prev_prices, 10)
        
        # 골든크로스 조건: 현재는 TEMA > DEMA, 전일은 TEMA < DEMA
        return current_tema > current_dema and prev_tema < prev_dema
    
    def meets_all_conditions(self, indicators: TechnicalIndicators, chart_data: List[Dict[str, Any]]) -> bool:
        """모든 조건 검증"""
        # 1. 골든크로스 조건
        golden_cross = self.check_golden_cross_condition(chart_data)
        
        # 2. MACD Oscillator > -50
        macd_condition = indicators.macd_oscillator > -50
        
        # 3. RSI(14) > 55
        rsi_condition = indicators.rsi_14 > 55
        
        # 4. 거래량 > 평균거래량(5) * 1.5
        volume_condition = indicators.volume_ratio > 1.5
        
        return golden_cross and macd_condition and rsi_condition and volume_condition
    
    def generate_trading_strategy(self, indicators: TechnicalIndicators, meets_conditions: bool) -> TradingStrategy:
        """매매 전략 생성"""
        if meets_conditions:
            # 신뢰도 계산 (각 지표의 강도 기반)
            confidence_factors = []
            
            # RSI 강도 (55~70 구간에서 높은 점수)
            rsi_strength = min(1.0, max(0.0, (indicators.rsi_14 - 55) / 15))
            confidence_factors.append(rsi_strength)
            
            # MACD 강도 (양수일수록 높은 점수)
            macd_strength = min(1.0, max(0.0, (indicators.macd_oscillator + 50) / 100))
            confidence_factors.append(macd_strength)
            
            # 거래량 강도 (1.5배 이상에서 점수)
            volume_strength = min(1.0, max(0.0, (indicators.volume_ratio - 1.5) / 1.0))
            confidence_factors.append(volume_strength)
            
            confidence = np.mean(confidence_factors)
            
            if confidence > 0.7:
                description = "강력한 상승 신호 - 적극 매수 고려"
            elif confidence > 0.5:
                description = "중간 상승 신호 - 단기 매수 고려"
            else:
                description = "약한 상승 신호 - 신중한 매수"
            
            return TradingStrategy(
                signal="BUY",
                description=description,
                confidence=confidence
            )
        else:
            return TradingStrategy(
                signal="HOLD",
                description="조건 미충족 - 관망",
                confidence=0.3
            )