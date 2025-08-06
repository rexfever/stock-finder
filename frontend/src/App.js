import React from 'react';
import StockScreener from './components/StockScreener';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                키움 주식 검색기
              </h1>
              <span className="ml-3 px-2 py-1 text-xs font-medium bg-kiwoom-100 text-kiwoom-800 rounded-full">
                BETA
              </span>
            </div>
            <div className="text-sm text-gray-500">
              키움증권 REST API 기반 조건검색
            </div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StockScreener />
      </main>
      
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>© 2024 키움 주식 검색기. 투자 판단은 본인의 책임입니다.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;