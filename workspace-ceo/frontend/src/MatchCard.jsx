import React from 'react'

function MatchCard({ match }) {
    return (
        <div className="match-card">
            <div className="match-header">
                <div className="league-info">
                    {match.league}
                </div>
                <div className="match-time">
                    {match.minute}'
                </div>
            </div>

            <div className="score-section">
                <div className="team">
                    <span className="team-name">{match.home_team}</span>
                    <span className="team-score">{match.home_score}</span>
                </div>

                <div className="score-divider">:</div>

                <div className="team">
                    <span className="team-name">{match.away_team}</span>
                    <span className="team-score">{match.away_score}</span>
                </div>
            </div>

            <div className="match-footer">
                <div className="match-id">ID: {match.match_id}</div>
                <div className="match-status">
                    <span className="live-badge">LIVE</span>
                </div>
            </div>
        </div>
    )
}

export default MatchCard
