export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          🐢 Turtle Trading Strategy Platform
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered stock analysis based on Turtle Trading Rules
        </p>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Welcome, Ying!</h2>
          <p className="text-gray-700 mb-4">
            This platform helps you analyze stocks using the famous Turtle Trading strategy.
          </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <a href="/analyze" className="block bg-blue-50 p-4 rounded-lg hover:bg-blue-100 transition-colors">
              <h3 className="font-bold text-blue-800 mb-2">📊 Stock Analysis</h3>
              <p className="text-sm text-gray-600">Analyze stock prices with Turtle Trading signals</p>
            </a>

            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-bold text-green-800 mb-2">📈 Entry/Exit Signals</h3>
              <p className="text-sm text-gray-600">Get real-time buy and sell recommendations</p>
            </div>

            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-bold text-purple-800 mb-2">📜 History</h3>
              <p className="text-sm text-gray-600">Track your analysis history</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}