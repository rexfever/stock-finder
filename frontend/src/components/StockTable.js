import React from 'react';

const StockTable = ({ stocks }) => {
  if (!stocks || stocks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
        <div className="text-gray-400 mb-4">
          <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <p className="text-gray-500">조건에 맞는 종목이 없습니다</p>
        <p className="text-sm text-gray-400 mt-1">다른 조건검색식을 시도해보세요</p>
      </div>
    );
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('ko-KR').format(price);
  };

  const formatPercent = (percent) => {
    const sign = percent >= 0 ? '+' : '';
    return `${sign}${percent.toFixed(2)}%`;
  };

  const getChangeColor = (percent) => {
    if (percent > 0) return 'text-profit';
    if (percent < 0) return 'text-loss';
    return 'text-neutral';
  };

  const getSignalBadge = (signal) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
    
    switch (signal) {
      case 'BUY':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'SELL':
        return `${baseClasses} bg-red-100 text-red-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const ProgressBar = ({ value, max = 1, color = "blue" }) => {
    const percentage = Math.min((value / max) * 100, 100);
    const colorClasses = {
      blue: "bg-blue-500",
      green: "bg-green-500",
      red: "bg-red-500",
      gray: "bg-gray-500"
    };

    return (
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className={`h-2 rounded-full transition-all duration-300 ${colorClasses[color]}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">
          검색 결과 ({stocks.length}개 종목)
        </h3>
        <p className="text-sm text-gray-500 mt-1">
          신뢰도 순으로 정렬되었습니다
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                종목정보
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                현재가
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                기술지표
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                매매전략
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                신뢰도
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {stocks.map((stock, index) => (
              <tr key={`${stock.stock_info.code}-${index}`} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {stock.stock_info.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {stock.stock_info.code}
                    </div>
                  </div>
                </td>
                
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm">
                    <div className="font-medium text-gray-900">
                      {formatPrice(stock.stock_info.price)}원
                    </div>
                    <div className={`text-sm ${getChangeColor(stock.stock_info.change_percent)}`}>
                      {formatPercent(stock.stock_info.change_percent)}
                    </div>
                  </div>
                </td>
                
                <td className="px-6 py-4">
                  <div className="text-xs space-y-1">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <span className="text-gray-500">TEMA(20):</span>
                        <span className="ml-1 font-medium">{stock.indicators.tema_20.toFixed(0)}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">DEMA(10):</span>
                        <span className="ml-1 font-medium">{stock.indicators.dema_10.toFixed(0)}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">MACD:</span>
                        <span className="ml-1 font-medium">{stock.indicators.macd_oscillator.toFixed(1)}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">RSI:</span>
                        <span className="ml-1 font-medium">{stock.indicators.rsi_14.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="mt-2">
                      <span className="text-gray-500">거래량 비율:</span>
                      <span className="ml-1 font-medium">{stock.indicators.volume_ratio.toFixed(1)}배</span>
                    </div>
                  </div>
                </td>
                
                <td className="px-6 py-4">
                  <div className="space-y-2">
                    <span className={getSignalBadge(stock.strategy.signal)}>
                      {stock.strategy.signal === 'BUY' ? '매수' : 
                       stock.strategy.signal === 'SELL' ? '매도' : '관망'}
                    </span>
                    <div className="text-xs text-gray-600 max-w-xs">
                      {stock.strategy.description}
                    </div>
                  </div>
                </td>
                
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-900">
                        {(stock.strategy.confidence * 100).toFixed(0)}%
                      </span>
                      {stock.meets_conditions && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                          ✓ 조건충족
                        </span>
                      )}
                    </div>
                    <ProgressBar 
                      value={stock.strategy.confidence} 
                      color={stock.strategy.confidence > 0.7 ? "green" : 
                             stock.strategy.confidence > 0.5 ? "blue" : "gray"} 
                    />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StockTable;