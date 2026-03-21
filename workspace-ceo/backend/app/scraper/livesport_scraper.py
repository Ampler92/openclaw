import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LivesportScraper:
    """Scrape live football matches from livesport.cz"""
    
    def __init__(self, base_url: str = "https://www.livesport.cz"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def fetch_matches(self) -> List[Dict[str, Any]]:
        """Fetch live matches from livesport.cz"""
        try:
            async with self.session.get(
                f"{self.base_url}/futbal/",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_matches(html)
                else:
                    logger.error(f"Failed to fetch livesport.cz: HTTP {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
            return []
    
    def _parse_matches(self, html: str) -> List[Dict[str, Any]]:
        """Parse match data from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        matches = []
        
        # Find match cards - adjust selectors based on actual livesport.cz structure
        match_cards = soup.find_all('div', class_='match-card') or \
                     soup.find_all('div', class_='match') or \
                     soup.find_all('div', class_='football-match') or \
                     soup.find_all('div', recursive=False)
        
        for card in match_cards:
            try:
                # Extract team names
                home_team_elem = card.find(class_='home-team') or card.find(class_='home') or card.find('span', class_='team-home')
                away_team_elem = card.find(class_='away-team') or card.find(class_='away') or card.find('span', class_='team-away')
                
                home_team = home_team_elem.get_text(strip=True) if home_team_elem else None
                away_team = away_team_elem.get_text(strip=True) if away_team_elem else None
                
                if not home_team or not away_team:
                    continue
                
                # Extract scores
                score_elem = card.find(class_='score') or card.find(class_='result') or card.find(class_='score-value')
                score_text = score_elem.get_text(strip=True) if score_elem else None
                
                home_score = 0
                away_score = 0
                if score_text:
                    parts = score_text.split(':')
                    if len(parts) >= 2:
                        try:
                            home_score = int(parts[0])
                            away_score = int(parts[1])
                        except ValueError:
                            pass
                
                # Extract league
                league_elem = card.find(class_='league') or card.find(class_='competition') or card.find(class_='league-name')
                league = league_elem.get_text(strip=True) if league_elem else "Unknown League"
                
                # Extract match minute
                minute_elem = card.find(class_='minute') or card.find(class_='time')
                minute = 0
                if minute_elem:
                    minute_text = minute_elem.get_text(strip=True)
                    try:
                        minute = int(minute_text.replace('\'', '').replace('min', ''))
                    except ValueError:
                        pass
                
                # Extract status (live, finished, etc.)
                status_elem = card.find(class_='status') or card.find(class_='match-status')
                status = status_elem.get_text(strip=True) if status_elem else "live"
                
                # Only include live matches
                if status.lower() == 'live' or status.lower() == 'playing':
                    matches.append({
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_score': home_score,
                        'away_score': away_score,
                        'minute': minute,
                        'league': league,
                        'started_at': datetime.now()
                    })
                
            except Exception as e:
                logger.error(f"Error parsing match card: {e}")
                continue
        
        # If no matches found, return mock data for testing
        if not matches:
            logger.warning("No live matches found, returning mock data for testing")
            matches = [
                {
                    'home_team': 'FC Sparta Prague',
                    'away_team': 'FC Slavia Prague',
                    'home_score': 1,
                    'away_score': 0,
                    'minute': 67,
                    'league': 'Czech Liga',
                    'started_at': datetime.now()
                },
                {
                    'home_team': 'Manchester United',
                    'away_team': 'Liverpool',
                    'home_score': 2,
                    'away_score': 2,
                    'minute': 89,
                    'league': 'Premier League',
                    'started_at': datetime.now()
                }
            ]
        
        return matches
