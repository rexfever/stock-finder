import axios from 'axios';

// API 기본 설정
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API 요청: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ 요청 에러:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API 응답: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ 응답 에러:', error.response?.data || error.message);
    
    // 에러 메시지 정리
    let errorMessage = '서버 오류가 발생했습니다.';
    
    if (error.response) {
      // 서버에서 응답한 에러
      errorMessage = error.response.data?.detail || 
                    error.response.data?.message || 
                    `서버 오류 (${error.response.status})`;
    } else if (error.request) {
      // 네트워크 오류
      errorMessage = '네트워크 연결을 확인해주세요.';
    }
    
    return Promise.reject(new Error(errorMessage));
  }
);

/**
 * 주식 서비스 클래스
 */
class StockService {
  /**
   * 서버 상태 확인
   */
  async checkHealth() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`서버 연결 실패: ${error.message}`);
    }
  }

  /**
   * 조건검색으로 종목 검색
   * @param {string} conditionName - 조건검색식 이름
   */
  async searchStocks(conditionName) {
    if (!conditionName?.trim()) {
      throw new Error('조건검색식 이름을 입력해주세요.');
    }

    try {
      const response = await api.post('/api/search', null, {
        params: { condition_name: conditionName.trim() }
      });
      
      return response.data;
    } catch (error) {
      // 키움 API 관련 에러 처리
      if (error.message.includes('인증') || error.message.includes('token')) {
        throw new Error('키움 API 인증이 필요합니다. 설정을 확인해주세요.');
      }
      
      if (error.message.includes('조건검색')) {
        throw new Error('조건검색식을 찾을 수 없습니다. HTS에서 저장된 이름을 확인해주세요.');
      }
      
      throw error;
    }
  }

  /**
   * 사용 가능한 조건검색식 목록 조회
   */
  async getAvailableConditions() {
    try {
      const response = await api.get('/api/conditions');
      return response.data;
    } catch (error) {
      throw new Error(`조건목록 조회 실패: ${error.message}`);
    }
  }
}

// 싱글톤 인스턴스 생성
const stockService = new StockService();

export default stockService;