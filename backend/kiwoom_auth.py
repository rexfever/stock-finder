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
        """액세스 토큰 발급/갱신"""
        current_time = datetime.now()
        
        # 캐시된 토큰이 있고 아직 유효하다면 재사용
        if ("access_token" in self.token_cache and 
            "expires_at" in self.token_cache and
            current_time < self.token_cache["expires_at"]):
            return self.token_cache["access_token"]
        
        # 새 토큰 발급
        url = f"{self.base_url}/oauth2/token"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)  # 기본 1시간
            
            # 토큰 캐시에 저장 (만료시간 10분 여유)
            self.token_cache = {
                "access_token": access_token,
                "expires_at": current_time + timedelta(seconds=expires_in - 600)
            }
            
            return access_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"토큰 발급 실패: {str(e)}")
    
    def get_auth_headers(self) -> dict:
        """인증 헤더 반환"""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }