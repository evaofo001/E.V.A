import { useState } from 'react'
import './App.css'

interface Message {
  id: string
  role: 'user' | 'eva'
  content: string
  timestamp: Date
}

const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : `https://${window.location.hostname.replace('-5000', '-8000')}`

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
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages([...messages, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          user_id: 'user_' + Math.random().toString(36).substr(2, 9)
        })
      })

      if (!response.ok) {
        throw new Error('Failed to get response from EVA')
      }

      const data = await response.json()
      
      const evaResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'eva',
        content: data.content,
        timestamp: new Date(data.timestamp)
      }
      
      setMessages(prev => [...prev, evaResponse])
    } catch (error) {
      console.error('Error communicating with EVA:', error)
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'eva',
        content: 'I apologize, but I encountered an error connecting to my core systems. Please ensure the backend is running and try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorResponse])
    } finally {
      setIsLoading(false)
    }
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
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !isLoading) {
                handleSend()
              }
            }}
            placeholder="Send a message to EVA..."
            className="message-input"
            disabled={isLoading}
          />
          <button onClick={handleSend} className="send-button" disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Send'}
          </button>
        </div>
      </div>

      <footer className="eva-footer">
        <div className="status">
          <span className="status-indicator active"></span>
          <span>System Status: Active</span>
        </div>
      </footer>
    </div>
  )
}

export default App
