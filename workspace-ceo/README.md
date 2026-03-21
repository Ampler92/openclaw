# Live Football Dashboard

A real-time dashboard for tracking live football matches.

## Features

- Real-time match updates
- Multi-league support
- Simple web UI
- RESTful API backend

## Quick Start

1. Start the backend:
   ```bash
   cd backend
   python app/main.py
   ```

2. Open the frontend:
   ```bash
   # Just open frontend/index.html in your browser
   ```

## Project Structure

```
live-fb-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── scraper/         # Web scraping logic
│   │   ├── cache/          # Cache management
│   │   └── api/            # API schemas
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Simple dashboard
│   └── package.json
└── README.md
```

## Next Steps

1. Implement actual livesport.cz scraper
2. Add WebSocket for real-time updates
3. Build React/Vue frontend
4. Add authentication
5. Deploy to production
