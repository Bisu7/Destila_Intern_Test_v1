import ExceptionInbox from './ExceptionInbox'
import './index.css'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Mini Exception Inbox</h1>
      </header>
      <main>
        <ExceptionInbox />
      </main>
    </div>
  )
}

export default App
