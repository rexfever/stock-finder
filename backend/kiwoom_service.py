import requests
import json
from typing import List, Dict, Any, Optional
from kiwoom_auth import KiwoomAuth
from stock_models import StockInfo


class KiwoomService:
    """키움증권 API 서비스"""
    
    def __init__(self):
        self.auth = KiwoomAuth()
        self.base_url = "https://openapi.kiwoom.com"
    
    def search_by_condition(self, condition_name: str) -> List[str]:
        """사용자 조건검색식으로 종목 검색"""
        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/inquire-psearch-result"
        headers = self.auth.get_auth_headers()
        headers["tr_id"] = "PSEARCH_RESULT"
        
        params = {
            "user_id": "",  # 사용자 ID (선택사항)
            "seq": "1",
            "condition_name": condition_name,
            "search_flag": "0"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("rt_cd") != "0":
                raise Exception(f"조건검색 실패: {data.get('msg1', 'Unknown error')}")
            
            # 응답에서 종목코드 리스트 추출
            output = data.get("output", [])
            stock_codes = [item.get("mksc_shrn_iscd", "") for item in output if item.get("mksc_shrn_iscd")]
            
            return stock_codes
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"조건검색 API 호출 실패: {str(e)}")
    
    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """종목의 현재가 정보 조회"""
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = self.auth.get_auth_headers()
        headers["tr_id"] = "FHKST01010100"
        
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("rt_cd") != "0":
                raise Exception(f"현재가 조회 실패: {data.get('msg1', 'Unknown error')}")
            
            output = data.get("output", {})
            return {
                "price": float(output.get("stck_prpr", 0)),  # 현재가
                "change_percent": float(output.get("prdy_ctrt", 0)),  # 등락률
                "volume": int(output.get("acml_vol", 0)),  # 누적거래량
                "high": float(output.get("stck_hgpr", 0)),  # 고가
                "low": float(output.get("stck_lwpr", 0)),  # 저가
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"현재가 조회 API 호출 실패: {str(e)}")
    
    def get_stock_chart_data(self, stock_code: str, period: str = "D", count: int = 30) -> List[Dict[str, Any]]:
        """종목의 차트 데이터 조회 (기술지표 계산용)"""
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        headers = self.auth.get_auth_headers()
        headers["tr_id"] = "FHKST03010100"
        
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code,
            "fid_input_date_1": "",  # 시작일자 (공백시 최근)
            "fid_input_date_2": "",  # 종료일자 (공백시 최근)
            "fid_period_div_code": period,  # D:일봉, W:주봉, M:월봉
            "fid_org_adj_prc": "1"  # 수정주가 반영
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("rt_cd") != "0":
                raise Exception(f"차트 데이터 조회 실패: {data.get('msg1', 'Unknown error')}")
            
            output = data.get("output2", [])
            chart_data = []
            
            for item in output[:count]:  # 최근 count개만 가져오기
                chart_data.append({
                    "date": item.get("stck_bsop_date", ""),
                    "open": float(item.get("stck_oprc", 0)),
                    "high": float(item.get("stck_hgpr", 0)),
                    "low": float(item.get("stck_lwpr", 0)),
                    "close": float(item.get("stck_clpr", 0)),
                    "volume": int(item.get("acml_vol", 0))
                })
            
            return chart_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"차트 데이터 조회 API 호출 실패: {str(e)}")
    
    def get_stock_name(self, stock_code: str) -> str:
        """종목코드로 종목명 조회"""
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/search-stock-info"
        headers = self.auth.get_auth_headers()
        headers["tr_id"] = "CTPF1002R"
        
        params = {
            "PRDT_TYPE_CD": "300",
            "MICR_DNVL_CNDC_1": stock_code
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("rt_cd") != "0":
                return f"종목{stock_code}"  # 조회 실패시 기본값
            
            output = data.get("output", [])
            if output:
                return output[0].get("prdt_abrv_name", f"종목{stock_code}")
            
            return f"종목{stock_code}"
            
        except requests.exceptions.RequestException as e:
            return f"종목{stock_code}"  # 에러시 기본값 반환