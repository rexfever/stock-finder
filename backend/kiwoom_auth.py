import os
import requests
import json
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class KiwoomAuth:
    """키움증권 OAuth 인증 관리"""
    
    def __init__(self):
        self.app_key = os.getenv("KIWOOM_APP_KEY")
        self.app_secret = os.getenv("KIWOOM_APP_SECRET")
        self.base_url = "https://openapi.kiwoom.com"
        self.token_cache = {}
        
        if not self.app_key or not self.app_secret:
            raise ValueError("키움 API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    def get_access_token(self) -> str:
        """
        키움증권 API 토큰 발급/갱신
        
        주의: 키움증권은 OAuth2 REST API를 공식적으로 지원하지 않습니다.
        실제로는 OCX(ActiveX) 기반의 Open API+를 사용해야 합니다.
        현재는 개발/테스트를 위한 모의 토큰을 반환합니다.
        """
        current_time = datetime.now()
        
        # 캐시된 토큰이 있고 아직 유효하다면 재사용
        if ("access_token" in self.token_cache and 
            "expires_at" in self.token_cache and
            current_time < self.token_cache["expires_at"]):
            return self.token_cache["access_token"]
        
        # 키움증권은 OAuth2 REST API를 지원하지 않으므로 모의 토큰 생성
        print("⚠️  키움증권은 OCX 기반 API를 사용합니다. 모의 토큰을 생성합니다.")
        
        # 모의 토큰 생성 (개발/테스트용)
        mock_token = f"MOCK_KIWOOM_TOKEN_{current_time.strftime('%Y%m%d_%H%M%S')}"
        
        # 토큰 캐시에 저장 (1시간 유효)
        self.token_cache = {
            "access_token": mock_token,
            "expires_at": current_time + timedelta(hours=1)
        }
        
        return mock_token
    
    def get_auth_headers(self) -> dict:
        """인증 헤더 반환"""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }