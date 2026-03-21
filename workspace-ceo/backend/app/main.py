from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import os
from datetime import datetime

app = FastAPI(title="Live Football Dashboard API")

# Mock data for now - will be replaced with actual scraper
class Match(BaseModel):
    id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    minute: int
    league: str
    started_at: datetime

class MatchDetails(BaseModel):
    match: Match
    stats: Optional[dict] = None

# In-memory cache
live_matches = {
    1: Match(
        id=1,
        home_team="FC Sparta Prague",
        away_team="FC Slavia Prague",
        home_score=1,
        away_score=0,
        minute=67,
        league="Czech Liga",
        started_at=datetime.now()
    ),
    2: Match(
        id=2,
        home_team="Manchester United",
        away_team="Liverpool",
        home_score=2,
        away_score=2,
        minute=89,
        league="Premier League",
        started_at=datetime.now()
    )
}

@app.get("/")
async def root():
    return {"message": "Live Football Dashboard API", "status": "running"}

@app.get("/api/live-matches", response_model=List[Match])
async def get_live_matches():
    """Get all live football matches"""
    return list(live_matches.values())

@app.get("/api/matches/{match_id}", response_model=Match)
async def get_match(match_id: int):
    """Get match details by ID"""
    if match_id not in live_matches:
        raise HTTPException(status_code=404, detail="Match not found")
    return live_matches[match_id]

@app.get("/api/matches/{match_id}/stats")
async def get_match_stats(match_id: int):
    """Get match statistics"""
    if match_id not in live_matches:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return {
        "possession": {"home": 55, "away": 45},
        "shots": {"home": 12, "away": 8},
        "shots_on_target": {"home": 5, "away": 3},
        "fouls": {"home": 8, "away": 11}
    }

if __name__ == "__main__":
    import uvicorn
    debug = os.getenv("DEBUG", "false").lower() == "true"
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=debug)
