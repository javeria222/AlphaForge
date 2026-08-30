import './App.css'
import VoiceInput from './components/VoiceInput'
import DecisionTimeline from './components/DecisionTimeline'
import AnswerCard from './components/AnswerCard'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">AlphaForge</h1>
          <p className="text-gray-600">Meeting Intelligence & Decision Extraction</p>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <VoiceInput />
          <DecisionTimeline />
        </div>
      </main>
    </div>
  )
}

export default App
