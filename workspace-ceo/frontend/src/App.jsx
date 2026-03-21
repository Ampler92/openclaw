import React, { useEffect, useState, useCallback } from 'react'
import MatchCard from './components/MatchCard.jsx'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
    const [matches, setMatches] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [lastUpdate, setLastUpdate] = useState(null)

    const fetchMatches = useCallback(async () => {
        try {
            setLoading(true)
            setError(null)
            
            const response = await fetch(`${API_BASE}/api/live-matches`)
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            
            const data = await response.json()
            setMatches(data)
            setLastUpdate(new Date())
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        fetchMatches()
        
        const interval = setInterval(fetchMatches, 5000)
        
        return () => clearInterval(interval)
    }, [fetchMatches])

    const formatTime = (date) => {
        if (!date) return ''
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    }

    return (
        <div className="dashboard-container">
            <header className="header">
                <h1>⚽ Live Football Dashboard</h1>
                <p>Real-time match updates</p>
            </header>

            <div className="status-bar">
                <div className="refresh-status">
                    <div className="refresh-indicator"></div>
                    <span>Auto-refreshing every 5 seconds</span>
                </div>
                <div className="update-time">
                    Last update: {formatTime(lastUpdate)}
                </div>
            </div>

            {loading && !error && (
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p style={{ marginTop: '20px' }}>Loading matches...</p>
                </div>
            )}

            {error && (
                <div className="error-state">
                    <h2>⚠️ Connection Error</h2>
                    <p>{error}</p>
                    <p style={{ marginTop: '15px', fontSize: '0.9rem' }}>
                        Make sure the backend server is running on port 8000
                    </p>
                    <button onClick={fetchMatches}>Try Again</button>
                </div>
            )}

            {!loading && !error && matches.length === 0 && (
                <div className="empty-state">
                    <h3>No Live Matches</h3>
                    <p>There are no live matches at the moment.</p>
                </div>
            )}

            {!loading && !error && matches.length > 0 && (
                <div className="matches-grid">
                    {matches.map((match) => (
                        <MatchCard key={match.match_id} match={match} />
                    ))}
                </div>
            )}
        </div>
    )
}

export default App
