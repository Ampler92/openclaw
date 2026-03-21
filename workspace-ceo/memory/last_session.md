# Live Football Dashboard - Project State

## Current Status (March 21, 2026)

**Project Type**: Live football match scraper and dashboard

**Architecture**:
- **Backend**: Python FastAPI (`backend/app/main.py`)
  - Endpoints: `/api/live-matches`, `/api/matches/{match_id}`, `/api/matches/{match_id}/stats`
  - Uses livesport.cz for scraping
  - Cache layer in `backend/app/cache/`
  - Scraper logic in `backend/app/scraper/`

- **Frontend**: JavaScript/TypeScript (`frontend/`)
  - Live match list with real-time updates
  - Match details and statistics view
  - Responsive design

## Recent Work

- Project structure initialized with backend and frontend folders
- Backend has API endpoints defined but may need implementation
- Frontend ready for dev server setup
- Configuration via `.env` file (LIVESPORT_URL, CACHE_TTL, UPDATE_INTERVAL)

## Next Steps (if any)

Waiting for user direction on what to implement or fix next.

## Files Referenced

- `backend/app/main.py` - FastAPI application entry point
- `backend/app/api/` - API route handlers
- `backend/app/scraper/` - Web scraping logic
- `backend/app/cache/` - Caching layer
- `frontend/` - Frontend application code

---
*Session started: March 21, 2026 02:11 UTC*
