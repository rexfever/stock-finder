#!/usr/bin/env python3
"""
키움증권 주식 검색기 백엔드 서버 시작 스크립트
"""

import os
import sys
import uvicorn
from pathlib import Path

# 현재 디렉터리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """메인 실행 함수"""
    # .env 파일 존재 확인
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("❌ .env 파일이 없습니다.")
        print("📁 .env.example을 참고하여 .env 파일을 생성하세요.")
        print("🔑 KIWOOM_APP_KEY와 KIWOOM_APP_SECRET을 설정해주세요.")
        return
    
    print("🚀 키움증권 주식 검색기 백엔드 서버를 시작합니다...")
    print("📊 API 문서: http://localhost:8000/docs")
    print("🏥 헬스체크: http://localhost:8000/health")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[str(current_dir)],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 서버가 종료되었습니다.")

if __name__ == "__main__":
    main()