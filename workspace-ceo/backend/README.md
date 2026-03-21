# Live Football Dashboard API

A FastAPI-based backend service that provides real-time football match data with caching and scheduling capabilities.

## Features

- Real-time football match tracking
- In-memory caching with configurable TTL
- Background task scheduling for live data updates
- RESTful API endpoints
- Environment-based configuration

## Setup Instructions

### Prerequisites

- Python 3.11+
- pip package manager

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Livesport scraper base URL
LIVESPORT_URL=https://www.livesport.cz

# Cache time-to-live in seconds (default: 60)
CACHE_TTL=60

# Data update interval in seconds (default: 30)
UPDATE_INTERVAL=30

# Enable debug mode (default: false)
DEBUG=false
```

**Environment Variables:**

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LIVESPORT_URL` | Base URL for the livesport scraper | `https://www.livesport.cz` | No |
| `CACHE_TTL` | Cache time-to-live in seconds | `60` | No |
| `UPDATE_INTERVAL` | Background update interval in seconds | `30` | No |
| `DEBUG` | Enable debug mode (`true`/`false`) | `false` | No |

## API Endpoints

### Base URL

```
http://localhost:8000
```

### Endpoints

#### `GET /`

**Description:** API health check and root endpoint.

**Response:**
```json
{
  "message": "Live Football Dashboard API",
  "status": "running"
}
```

---

#### `GET /api/live-matches`

**Description:** Get all live football matches.

**Response Code:** `200 OK`

**Response Schema:** Array of `Match` objects.

**Example Response:**
```json
[
  {
    "id": 1,
    "home_team": "FC Sparta Prague",
    "away_team": "FC Slavia Prague",
    "home_score": 1,
    "away_score": 0,
    "minute": 67,
    "league": "Czech Liga",
    "started_at": "2026-03-21T01:30:00"
  },
  {
    "id": 2,
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "home_score": 2,
    "away_score": 2,
    "minute": 89,
    "league": "Premier League",
    "started_at": "2026-03-21T01:15:00"
  }
]
```

**Match Object Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique match identifier |
| `home_team` | str | Home team name |
| `away_team` | str | Away team name |
| `home_score` | int | Home team current score |
| `away_score` | int | Away team current score |
| `minute` | int | Current match minute |
| `league` | str | League/competition name |
| `started_at` | datetime | Match start timestamp |

---

#### `GET /api/matches/{match_id}`

**Description:** Get detailed information for a specific match by ID.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `match_id` | int | The unique match identifier (required) |

**Response Code:** `200 OK` or `404 Not Found`

**Success Response:**
```json
{
  "id": 1,
  "home_team": "FC Sparta Prague",
  "away_team": "FC Slavia Prague",
  "home_score": 1,
  "away_score": 0,
  "minute": 67,
  "league": "Czech Liga",
  "started_at": "2026-03-21T01:30:00"
}
```

**Error Response (404):**
```json
{
  "detail": "Match not found"
}
```

---

#### `GET /api/matches/{match_id}/stats`

**Description:** Get detailed statistics for a specific match.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `match_id` | int | The unique match identifier (required) |

**Response Code:** `200 OK` or `404 Not Found`

**Success Response:**
```json
{
  "possession": {
    "home": 55,
    "away": 45
  },
  "shots": {
    "home": 12,
    "away": 8
  },
  "shots_on_target": {
    "home": 5,
    "away": 3
  },
  "fouls": {
    "home": 8,
    "away": 11
  }
}
```

**Statistics Object Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `possession` | object | Ball possession percentage |
| `shots` | object | Total shots taken |
| `shots_on_target` | object | Shots on target count |
| `fouls` | object | Fouls committed |

**Error Response (404):**
```json
{
  "detail": "Match not found"
}
```

---

### API Documentation

Interactive API documentation is available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Running the Server

### Development Mode

```bash
cd backend
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Recommended Production Flags:**

| Flag | Description |
|------|-------------|
| `--host 0.0.0.0` | Listen on all network interfaces |
| `--port 8000` | HTTP port (change if needed) |
| `--workers N` | Number of worker processes (recommended: 2-4) |
| `--access-log` | Enable access logging |
| `--log-level info` | Set logging level |

### Using a Process Manager (Recommended for Production)

**Systemd Service Example:**

Create `/etc/systemd/system/football-api.service`:

```ini
[Unit]
Description=Live Football Dashboard API
After=network.target

[Service]
User=klaus-silhan
WorkingDirectory=/home/klaus-silhan/.openclaw/workspace-ceo/backend
ExecStart=/home/klaus-silhan/.openclaw/workspace-ceo/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable football-api
sudo systemctl start football-api
sudo systemctl status football-api
```

## Configuration Options

### Runtime Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `LIVESPORT_URL` | string | `https://www.livesport.cz` | Base URL for live score scraping |
| `CACHE_TTL` | int | `60` | Cache expiration time in seconds |
| `UPDATE_INTERVAL` | int | `30` | Background data update interval in seconds |
| `DEBUG` | boolean | `false` | Enable debug mode (auto-reload, debug logs) |

### Cache Configuration

The API uses an in-memory cache with the following characteristics:

- **Storage:** Dictionary-based in-memory storage
- **TTL:** Configurable per-entry or default from `CACHE_TTL`
- **Auto-expiration:** Expired entries are automatically removed on access
- **Operations:** `set()`, `get()`, `delete()`, `clear()`

### Background Tasks

The application automatically starts background tasks for:

1. **Live data fetching** - Periodically fetches updated match data
2. **Session management** - Manages HTTP sessions for scraping

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic response schemas
│   ├── cache/
│   │   ├── __init__.py
│   │   └── cache_manager.py # In-memory cache implementation
│   └── scraper/
│       ├── __init__.py
│       ├── livesport_scraper.py  # Livesport.cz scraper
│       └── utils.py         # Scraper utilities
├── .env.example             # Environment template
├── .env                     # Your environment config (create from .env.example)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Dependencies

### Backend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.109.0 | Web framework |
| `uvicorn[standard]` | 0.27.0 | ASGI server |
| `aiohttp` | 3.9.1 | Async HTTP client |
| `scrapy` | 2.11.0 | Web scraping framework |
| `redis` | 5.0.1 | Cache backend (optional) |
| `python-dotenv` | 1.0.0 | Environment variable management |
| `pydantic` | 2.5.3 | Data validation and settings |
| `schedule` | 1.2.1 | Background task scheduling |

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `404` | Resource not found |
| `500` | Internal server error |

### Error Response Format

```json
{
  "detail": "Error description message"
}
```

## Production Checklist

- [ ] Set `DEBUG=false` in `.env`
- [ ] Configure production server (uWSGI, Gunicorn, or multi-worker uvicorn)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up logging and monitoring
- [ ] Implement proper error tracking (Sentry, etc.)
- [ ] Add authentication/authorization if needed
- [ ] Implement rate limiting
- [ ] Configure proper CORS headers
- [ ] Set up database persistence (replace in-memory storage)
- [ ] Implement proper scraper logic for production data

## Troubleshooting

### Common Issues

**1. Port already in use**

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

**2. Module not found errors**

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**3. Environment variables not loading**

```bash
# Verify .env file exists in backend directory
ls -la .env

# Ensure python-dotenv is imported in main.py
```

**4. Scraper not fetching data**

- Check `LIVESPORT_URL` is accessible
- Review scraper implementation in `app/scraper/livesport_scraper.py`
- Check network connectivity and firewall rules

## License

Proprietary - All rights reserved.

## Support

For issues and questions, contact the development team.

---

*Generated for Live Football Dashboard Project*
