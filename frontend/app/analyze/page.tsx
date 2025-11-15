'use client'

import { useState } from 'react'

export default function AnalyzePage() {
  // State: 存储用户输入的股票代码
  const [symbol, setSymbol] = useState('')

  // State: 存储是否正在加载
  const [loading, setLoading] = useState(false)

  // State: 存储分析结果
  const [result, setResult] = useState(null)

  // 处理表单提交
  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setLoading(true)

  try {
    // 调用后端API
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symbol: symbol,
        period: '2mo',
        entry_period: 20,
        exit_period: 10
      })
    })

    if (!response.ok) {
      throw new Error('Analysis failed')
    }

    const data = await response.json()
    setResult(data)
  } catch (error) {
    console.error('Error:', error)
    alert('Failed to analyze stock. Please try again.')
  } finally {
    setLoading(false)
  }
}

  return (
    <main className="min-h-screen p-8 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto">
        {/* 标题 */}
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          📊 Stock Analysis
        </h1>
        <p className="text-gray-600 mb-8">
          Enter a stock symbol to analyze with Turtle Trading strategy
        </p>

        {/* 分析表单 */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="symbol" className="block text-sm font-medium text-gray-700 mb-2">
                Stock Symbol
              </label>
              <input
                type="text"
                id="symbol"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
                placeholder="e.g., AAPL, TSLA, MSFT"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder:text-gray-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Analyzing...' : 'Analyze Stock'}
            </button>
          </form>
        </div>

        {/* 结果展示 */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Analysis Result</h2>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm text-gray-600">Symbol</p>
                <p className="text-xl font-bold text-gray-900">{result.symbol}</p>
              </div>

              <div className="bg-green-50 p-4 rounded">
                <p className="text-sm text-gray-600">Signal</p>
                <p className="text-xl font-bold text-green-700">{result.signal}</p>
              </div>

              <div className="bg-blue-50 p-4 rounded">
                <p className="text-sm text-gray-600">Current Price</p>
                <p className="text-xl font-bold text-blue-700">${result.current_price}</p>
              </div>

              <div className="bg-purple-50 p-4 rounded">
                <p className="text-sm text-gray-600">Entry Price</p>
                <p className="text-xl font-bold text-purple-700">${result.entry_price}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}