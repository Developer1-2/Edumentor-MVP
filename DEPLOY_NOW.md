# 🚀 Edumentor MVP — Deploy Now Checklist

## Status: ✅ Ready for Production

All components are configured and ready. Follow this checklist to deploy in under 10 minutes.

---

## Pre-Deployment (5 min)

- [ ] **Ensure Git is installed** on your machine
  - Download from git-scm.com if not already installed
  - Restart PowerShell after installation

- [ ] **GitHub Account Ready**
  - Create GitHub account if you don't have one (github.com)

- [ ] **Render Account Ready**
  - Create free Render account (render.com)

---

## Step 1: Push Code to GitHub (3 min)

Run these commands in PowerShell from project root:

```powershell
cd "c:\Users\OMARA DANIEL\Desktop\NEONVERSE TECHNOLOGIES\MVP\edumentor_mvp_backennd"

# Configure Git user (one-time)
git config --global user.email "your_email@example.com"
git config --global user.name "Your Name"

# Initialize repo
git init

# Add all files
git add .

# Commit
git commit -m "Edumentor MVP - Ready for production"

# Add GitHub remote (replace YOUR_USER with your GitHub username)
git remote add origin https://github.com/YOUR_USER/edumentor-mvp.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**First push:** Git will ask for your GitHub credentials. Use your GitHub username and a **Personal Access Token** (create one at github.com/settings/tokens).

---

## Step 2: Deploy to Render (5 min)

1. Go to **render.com** → Sign in / Create account
2. Click **"New +"** in top-right
3. Select **"Web Service"**
4. Click **"Connect account"** → Authorize GitHub
5. Select your **`edumentor-mvp`** repository
6. Fill in details:
   - **Name**: `edumentor-mvp-api`
   - **Environment**: `Python 3`
   - **Region**: `Oregon` (or your region)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker routes.main:app --bind 0.0.0.0:$PORT --workers 4`
7. Click **"Create Web Service"**

Render will start building. Watch the **Logs** tab. After 2-3 minutes, you should see:
- ✅ Build succeeds
- ✅ Service shows "Live" status
- ✅ Your app is live at: `https://edumentor-mvp-api.onrender.com`

---

## Step 3: Verify Deployment (1 min)

Open in browser:

```
https://edumentor-mvp-api.onrender.com/
```

You should see:
```json
{"message": "Welcome to Edumentor MVP API"}
```

Also check:
- API Docs: `https://edumentor-mvp-api.onrender.com/docs`
- Frontend: `https://edumentor-mvp-api.onrender.com/index.html`

---

## Step 4: (Optional) Add Production Database

For production, use Render's managed Postgres instead of SQLite:

1. On your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `edumentor-db`
3. Click **"Create Database"**
4. Copy the **Internal Database URL**
5. Go back to your web service → **Environment**
6. Update **`DATABASE_URL`** to the Postgres URL
7. Click **"Save"** — Render will redeploy

---

## Step 5: (Optional) Set Payment Credentials

If you have Eversend API credentials:

1. Go to your web service → **Environment**
2. Add:
   - `EVERSEND_API_KEY`: (your API key)
   - `EVERSEND_SECRET`: (your secret)
3. Click **"Save"**

---

## What You Now Have

✅ **Live API** at `https://edumentor-mvp-api.onrender.com`
✅ **Static frontend** served from the same domain (no separate frontend deployment needed)
✅ **Database ready** (local SQLite or managed Postgres)
✅ **Auto-deploy** on every GitHub push to `main` branch

---

## Testing Your Live App

1. Open `https://edumentor-mvp-api.onrender.com/index.html`
2. Click **"Register as Teacher"**
3. Fill form and submit
4. Try login, job posting, applications — all functions should work

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check Render logs. Ensure `requirements.txt` exists at project root. |
| 404 on `/docs` | Normal on Render during first build. Wait 1-2 minutes. |
| API returns 500 | Check Render logs for Python errors. Common: missing env var. |
| CORS errors in console | Already configured with `*` origin — should be fine. |

---

## Next Steps (After Deployment)

1. **Test payment flow** with real Eversend or test account
2. **Monitor logs** on Render dashboard for errors
3. **Set custom domain** (Render → Settings → Custom Domains)
4. **Add email notifications** (optional enhancement)
5. **Track user metrics** and improve UX

---

## You're Done! 🎉

Your Edumentor MVP is now **live on the internet** and ready for users.

**Share your app link**: `https://edumentor-mvp-api.onrender.com/`

Questions? Check `RENDER_DEPLOY.md` for detailed Render instructions.
