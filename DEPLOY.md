Edumentor MVP — Deployment Notes

Goal
- Run the FastAPI app in a production-like environment and expose the API and static HTML pages.

Prerequisites
- Python 3.10+ installed
- Create and activate a virtual environment

Windows (PowerShell)
1. Create & activate venv
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Install dependencies
   pip install -r requirements.txt

3. Start the API (production-like)
   .\start_production.bat

This runs:
   python -m uvicorn routes.main:app --host 0.0.0.0 --port 8000 --workers 4

Notes & Recommendations
- For real production, consider:
  - Running behind a reverse proxy (NGINX) and using HTTPS.
  - Using a process manager (systemd on Linux, NSSM or Windows Service wrapper on Windows).
  - Running inside Docker for portability.
  - Using a proper RDBMS (Postgres) instead of local SQLite for multi-instance deployments.

- CORS is permissive in `routes/main.py` (allows `*`) — tighten this for production to your actual frontend origin.

Testing
- Once running, open browser at `http://localhost:8000/` and the static HTML files (served separately by a static file server or by opening `index.html` directly).
- API docs: `http://localhost:8000/docs`

Optional: Docker
- If you want, I can create a minimal `Dockerfile` and `docker-compose.yml` so you can ship this as a container.

Render (render.com) Quick Deploy
- Create a new Web Service in Render and connect your repository.
- Use the following "Build Command":
   - `pip install -r requirements.txt`
- Use the following "Start Command":
   - `gunicorn -k uvicorn.workers.UvicornWorker routes.main:app --bind 0.0.0.0:$PORT --workers 4`
- Alternatively add the provided `render.yaml` to the repo and Render will read it during the first deployment.
- Add required environment variables in the Render service settings:
   - `DATABASE_URL` (e.g. `sqlite:///./edumentor.db` or a Postgres URL)
   - `EVERSEND_API_KEY`, `EVERSEND_SECRET` (if using payments in production)
   - `SECRET_KEY` (app secret for sessions / tokens if used)

Notes specific to Render
- If you plan to use the free plan, be aware of sleep/idle behavior. Use a paid plan for production uptime.
- For SQLite, the database is ephemeral on multiple instances. Use managed Postgres for persistent data across deploys.
