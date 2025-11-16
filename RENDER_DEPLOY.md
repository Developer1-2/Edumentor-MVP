# Deploy Edumentor MVP to Render — Quick Start

## Prerequisites
- GitHub account
- Render account (render.com)
- Project folder ready on your machine

## Step 1: Create GitHub Repository (One-Time)

1. Go to **github.com** → Sign in
2. Click **"New repository"** (top-left)
3. Repository name: `edumentor-mvp`
4. Description: `Edumentor MVP - Teacher-School Job Platform`
5. **Public** (so Render can access it)
6. Click **"Create repository"**
7. Copy the **HTTPS clone URL** (looks like `https://github.com/YOUR_USER/edumentor-mvp.git`)

## Step 2: Push Code to GitHub (One-Time)

From your project root folder (PowerShell):

```powershell
# Navigate to project
cd "c:\Users\OMARA DANIEL\Desktop\NEONVERSE TECHNOLOGIES\MVP\edumentor_mvp_backennd"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial Edumentor MVP commit"

# Add remote and push (replace YOUR_USER/edumentor-mvp with your repo URL)
git remote add origin https://github.com/YOUR_USER/edumentor-mvp.git
git branch -M main
git push -u origin main
```

> **On first push:** Git may ask for GitHub credentials. Use your GitHub username and a **Personal Access Token** (generate one at github.com/settings/tokens).

## Step 3: Deploy to Render (One-Time Setup)

1. Go to **render.com** → Sign in (or create account)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub account if prompted
4. Select your `edumentor-mvp` repository
5. Fill in details:
   - **Name**: `edumentor-mvp-api`
   - **Environment**: `Python 3`
   - **Region**: `Oregon` (or your preferred region)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker routes.main:app --bind 0.0.0.0:$PORT --workers 4`
6. Click **"Create Web Service"**

## Step 4: Set Environment Variables on Render

Once the service is created:

1. Go to your service dashboard on Render
2. Click **"Environment"** (left sidebar)
3. Add these variables:
   - **`DATABASE_URL`**: Leave blank for now (or use SQLite: `sqlite:///./edumentor.db`)
     - *Later: Replace with a managed Postgres URL from Render*
   - **`EVERSEND_API_KEY`**: (your Eversend API key, or leave blank for testing)
   - **`EVERSEND_SECRET`**: (your Eversend secret, or leave blank for testing)
   - **`SECRET_KEY`**: `replace-with-secret-key-later`
4. Click **"Save"**

Render will auto-redeploy with the new env vars.

## Step 5: Connect Postgres Database (Optional but Recommended for Production)

1. On Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `edumentor-db`
3. **Region**: same as your web service
4. Click **"Create Database"**
5. Once created, copy the **Internal Database URL**
6. Go back to your web service, click **"Environment"**
7. Update **`DATABASE_URL`** with the Postgres URL you copied
8. Click **"Save"** — Render will redeploy

## Step 6: Monitor Deployment

1. On your web service page, watch the **"Logs"** tab
2. After a few minutes, you should see:
   - `Starting Gunicorn...`
   - Service becomes **"Live"** (green indicator)
3. Your API is now live at: `https://edumentor-mvp-api.onrender.com`

Test it:
- Open browser: `https://edumentor-mvp-api.onrender.com/`
- Check docs: `https://edumentor-mvp-api.onrender.com/docs`

## Step 7: Point Frontend to Deployed API

Open your HTML files and update the API base URL:

- Find lines like `const API_BASE = ...` in JavaScript
- Replace `http://127.0.0.1:8000` with `https://edumentor-mvp-api.onrender.com`
- Or set a global in each HTML file:
  ```javascript
  window._API_BASE_ = 'https://edumentor-mvp-api.onrender.com';
  ```

Commit and push the changes:
```powershell
git add .
git commit -m "Update API endpoints to production"
git push origin main
```

Render will auto-redeploy.

## Step 8: Serve Frontend

You have two options:

### Option A: Serve HTML from Render (Add to Routes)
Add a static file handler in `routes/main.py` to serve the HTML files. (I can do this if you want.)

### Option B: Deploy Frontend Separately
- Use **Vercel**, **Netlify**, or **GitHub Pages** to host the static HTML files
- Update API URLs to point to your Render API
- Recommend: Netlify (drag-and-drop, free, HTTPS included)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | Check Render logs. Ensure `requirements.txt` is at project root. |
| `ModuleNotFoundError` | Verify `PYTHONPATH` or import paths in `routes/main.py`. |
| Database errors | Ensure `DATABASE_URL` is set correctly in Environment. |
| CORS errors | Update `allow_origins` in `routes/main.py` to include your frontend domain. |
| Service goes to sleep | Use Render's **paid plan** or upgrade to prevent idle shutdown. |

## Next Steps

After successful deployment:
1. Test registration, login, job posting, applications on production
2. Set up real Eversend credentials for payments
3. Add email notifications
4. Monitor logs and errors on Render dashboard
5. Set up custom domain if needed (Render → Settings → Custom Domains)

---

**Status**: Ready to deploy! Follow steps 1–8 above and your MVP will be live.
