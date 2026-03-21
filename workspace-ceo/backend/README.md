# Live Football Dashboard - Backend

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

4. Run the server:
   ```bash
   python app/main.py
   ```

## API Endpoints

- `GET /api/live-matches` - Get all live football matches
- `GET /api/matches/{match_id}` - Get match details
- `GET /api/matches/{match_id}/stats` - Get match statistics

## Configuration

Set these in `.env`:
- `LIVESPORT_URL` - Base URL for scraping
- `CACHE_TTL` - Cache TTL in seconds (default: 60)
- `UPDATE_INTERVAL` - How often to refresh data (default: 30 seconds)
