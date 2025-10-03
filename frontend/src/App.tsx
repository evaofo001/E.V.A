import { useState } from 'react'
import './App.css'

interface Message {
  id: string
  role: 'user' | 'eva'
  content: string
  timestamp: Date
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'eva',
      content: 'Hello! I am EVA - Evolutionary Virtual Android. I am designed to observe, learn, adapt, and evolve autonomously. How may I assist you today?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages([...messages, userMessage])
    setInput('')

    setTimeout(() => {
      const evaResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'eva',
        content: 'I am currently in development mode. My full cognitive systems are being initialized. Please check back soon as I continue to evolve.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, evaResponse])
    }, 1000)
  }

  return (
    <div className="eva-container">
      <header className="eva-header">
        <h1>EVA</h1>
        <p className="subtitle">Evolutionary Virtual Android</p>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.role}`}>
              <div className="message-header">
                <strong>{msg.role === 'eva' ? 'EVA' : 'You'}</strong>
                <span className="timestamp">
                  {msg.timestamp.toLocaleTimeString()}
                </span>
              </div>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Send a message to EVA..."
            className="message-input"
          />
          <button onClick={handleSend} className="send-button">
            Send
          </button>
        </div>
      </div>

      <footer className="eva-footer">
        <div className="status">
          <span className="status-indicator active"></span>
          <span>System Status: Initializing</span>
        </div>
      </footer>
    </div>
  )
}

export default App
