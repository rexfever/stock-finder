import React, { useState } from 'react';
import LoadingSpinner from './LoadingSpinner';

const SearchForm = ({ onSearch, loading = false }) => {
  const [conditionName, setConditionName] = useState('사용자_조건검색식');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (conditionName.trim() && !loading) {
      onSearch(conditionName.trim());
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          조건검색
        </h2>
        <div className="text-sm text-gray-500">
          키움 HTS에서 저장한 조건검색식 이름 입력
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="condition-name" className="block text-sm font-medium text-gray-700 mb-2">
            조건검색식 이름
          </label>
          <input
            id="condition-name"
            type="text"
            value={conditionName}
            onChange={(e) => setConditionName(e.target.value)}
            placeholder="예: 사용자_조건검색식"
            disabled={loading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 
                     focus:outline-none focus:ring-kiwoom-500 focus:border-kiwoom-500 
                     disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <p className="mt-1 text-xs text-gray-500">
            💡 키움 HTS에서 "조건검색" → "조건검색식 저장"으로 미리 저장해둔 이름을 입력하세요
          </p>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            <div className="mb-1">🔍 검색 조건:</div>
            <ul className="list-disc list-inside space-y-1 text-xs text-gray-500">
              <li>TEMA(20) > DEMA(10) 골든크로스</li>
              <li>MACD Oscillator > -50</li>
              <li>RSI(14) > 55</li>
              <li>거래량 > 평균거래량(5일) × 1.5</li>
            </ul>
          </div>
          
          <button
            type="submit"
            disabled={loading || !conditionName.trim()}
            className="bg-kiwoom-600 hover:bg-kiwoom-700 disabled:bg-gray-400 
                     text-white font-medium py-2 px-6 rounded-md transition-colors
                     disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {loading ? (
              <>
                <LoadingSpinner size="small" />
                <span>검색 중...</span>
              </>
            ) : (
              <span>조건검색 실행</span>
            )}
          </button>
        </div>
      </form>
      
      {loading && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center">
            <LoadingSpinner size="small" />
            <div className="ml-3 text-sm text-blue-700">
              <p className="font-medium">검색을 진행하고 있습니다...</p>
              <p className="text-xs mt-1">키움 API 호출 및 기술지표 분석 중 (최대 30초 소요)</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchForm;