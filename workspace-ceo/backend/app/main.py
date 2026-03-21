from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import os
from datetime import datetime
import logging

from app.scraper.livesport_scraper import LivesportScraper
from app.scraper.utils import get_cache_key

app = FastAPI(title="Live Football Dashboard API")

logger = logging.getLogger(__name__)

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

# In-memory cache for matches
live_matches: dict = {}
match_counter = 0

# Scraper instance
scraper: Optional[LivesportScraper] = None

async def fetch_live_matches():
    """Fetch live matches from livesport.cz"""
    global live_matches, match_counter
    
    try:
        if scraper is None:
            logger.warning("Scraper not initialized")
            return []
        
        matches_data = await scraper.fetch_matches()
        
        if not matches_data:
            logger.warning("No matches found")
            return []
        
        # Clear existing matches
        live_matches.clear()
        
        # Add new matches with unique IDs
        for idx, match_data in enumerate(matches_data, 1):
            match_counter = max(match_counter, idx) + 1
            match_id = match_counter
            
            match = Match(
                id=match_id,
                home_team=match_data['home_team'],
                away_team=match_data['away_team'],
                home_score=match_data['home_score'],
                away_score=match_data['away_score'],
                minute=match_data.get('minute', 0),
                league=match_data.get('league', 'Unknown League'),
                started_at=match_data.get('started_at', datetime.now())
            )
            live_matches[match_id] = match
        
        logger.info(f"Fetched {len(matches_data)} live matches")
        return list(live_matches.values())
        
    except Exception as e:
        logger.error(f"Error fetching matches: {e}")
        return []

@app.on_event("startup")
async def startup():
    """Initialize scraper on startup"""
    global scraper
    
    scraper = LivesportScraper()
    await scraper.initialize()
    
    # Fetch initial data
    await fetch_live_matches()
    
    # Start background task to update matches
    asyncio.create_task(update_matches_loop())

async def update_matches_loop():
    """Background task to update matches every 30 seconds"""
    while True:
        await asyncio.sleep(30)
        logger.info("Updating live matches...")
        await fetch_live_matches()

@app.get("/")
async def root():
    return {"message": "Live Football Dashboard API", "status": "running"}

@app.get("/api/live-matches", response_model=List[Match])
async def get_live_matches():
    """Get all live football matches"""
    if not live_matches:
        logger.info("No matches cached, fetching from scraper")
        await fetch_live_matches()
    
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
    
    # Generate random stats for demo
    import random
    home_possession = random.randint(40, 60)
    
    return {
        "possession": {
            "home": home_possession,
            "away": 100 - home_possession
        },
        "shots": {
            "home": random.randint(5, 15),
            "away": random.randint(3, 12)
        },
        "shots_on_target": {
            "home": random.randint(2, 8),
            "away": random.randint(1, 6)
        },
        "fouls": {
            "home": random.randint(5, 15),
            "away": random.randint(4, 14)
        }
    }

@app.get("/api/health")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "matches_cached": len(live_matches),
        "scraper_initialized": scraper is not None
    }

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    if scraper:
        await scraper.close()

if __name__ == "__main__":
    import uvicorn
    debug = os.getenv("DEBUG", "false").lower() == "true"
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=debug)
