import React, { useState, useEffect } from 'react';
import SearchForm from './SearchForm';
import StockTable from './StockTable';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import stockService from '../services/stockService';

const StockScreener = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchInfo, setSearchInfo] = useState(null);

  // 컴포넌트 마운트 시 서버 상태 확인
  useEffect(() => {
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      const health = await stockService.checkHealth();
      console.log('서버 상태:', health);
    } catch (error) {
      console.warn('서버 상태 확인 실패:', error.message);
    }
  };

  const handleSearch = async (conditionName) => {
    setLoading(true);
    setError(null);
    setStocks([]);
    setSearchInfo(null);

    try {
      console.log(`조건검색 시작: ${conditionName}`);
      const startTime = Date.now();
      
      const response = await stockService.searchStocks(conditionName);
      
      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(1);
      
      if (response.success) {
        setStocks(response.stocks || []);
        setSearchInfo({
          conditionName,
          totalCount: response.total_count || 0,
          searchTime: response.search_time,
          duration
        });
        
        console.log(`✅ 검색 완료: ${response.stocks?.length || 0}개 종목, ${duration}초`);
      } else {
        throw new Error(response.message || '검색에 실패했습니다.');
      }
    } catch (error) {
      console.error('검색 실패:', error);
      setError(error.message);
      setStocks([]);
      setSearchInfo(null);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    if (searchInfo?.conditionName) {
      handleSearch(searchInfo.conditionName);
    }
  };

  return (
    <div className="space-y-6">
      {/* 검색 폼 */}
      <SearchForm onSearch={handleSearch} loading={loading} />
      
      {/* 검색 정보 */}
      {searchInfo && !loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4 text-sm text-blue-700">
              <span>📊 검색조건: <strong>{searchInfo.conditionName}</strong></span>
              <span>🎯 총 {searchInfo.totalCount}개 종목</span>
              <span>⏱️ {searchInfo.duration}초 소요</span>
            </div>
            {searchInfo.totalCount > 0 && (
              <button
                onClick={handleRetry}
                className="text-blue-600 hover:text-blue-800 font-medium text-sm"
              >
                🔄 새로고침
              </button>
            )}
          </div>
        </div>
      )}
      
      {/* 로딩 상태 */}
      {loading && (
        <div className="bg-white rounded-lg shadow-sm border">
          <LoadingSpinner 
            message="키움 API에서 데이터를 가져오고 있습니다..." 
            size="large" 
          />
        </div>
      )}
      
      {/* 에러 상태 */}
      {error && !loading && (
        <ErrorMessage error={error} onRetry={handleRetry} />
      )}
      
      {/* 검색 결과 테이블 */}
      {!loading && !error && (stocks.length > 0 || searchInfo) && (
        <StockTable stocks={stocks} />
      )}
      
      {/* 초기 상태 안내 */}
      {!loading && !error && !searchInfo && stocks.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} 
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            키움 주식 검색기에 오신 것을 환영합니다
          </h3>
          <p className="text-gray-600 mb-4">
            조건검색식을 입력하고 검색 버튼을 눌러 시작하세요
          </p>
          <div className="bg-gray-50 rounded-lg p-4 text-left max-w-md mx-auto">
            <h4 className="font-medium text-gray-900 mb-2">💡 사용 방법:</h4>
            <ol className="text-sm text-gray-600 space-y-1 list-decimal list-inside">
              <li>키움 HTS에서 조건검색식을 미리 저장해두세요</li>
              <li>저장한 조건검색식 이름을 위 폼에 입력하세요</li>
              <li>"조건검색 실행" 버튼을 클릭하세요</li>
              <li>조건에 맞는 종목들과 분석 결과를 확인하세요</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockScreener;