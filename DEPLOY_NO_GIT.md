# Deploy Without Git CLI — Use GitHub Web UI

## Option 1: Deploy via GitHub Web Interface (Fastest — No Git Install Needed)

### Step 1: Create GitHub Repository

1. Go to **github.com** → Sign in (create account if needed)
2. Click **"+"** (top-right) → **"New repository"**
3. **Repository name**: `edumentor-mvp`
4. **Description**: `Edumentor MVP - Teacher-School Job Platform`
5. **Visibility**: **Public**
6. Click **"Create repository"**

### Step 2: Upload Files via GitHub Web UI

1. On your new repo page, click **"uploading an existing file"** (or **"Add file"** → **"Upload files"**)
2. Drag & drop all files from your project folder OR click **"choose your files"** and select them
3. Select all `.py`, `.html`, `.txt`, `.yml`, `.md`, `.bat`, `.ini` files from your project
4. Write commit message: `"Edumentor MVP - Initial commit"`
5. Click **"Commit changes"**

**Repeat for subdirectories:**
- Upload `routes/` folder contents
- Upload `scripts/` folder contents
- Upload `alembic/` folder contents
- Upload `utils/` folder contents

### Step 3: Add `.gitignore` via Web UI

1. Click **"Add file"** → **"Create new file"**
2. Name: `.gitignore`
3. Copy content from `DEPLOY_NOW.md` → paste the `.gitignore` content
4. Commit message: `"Add .gitignore"`
5. Click **"Commit new file"**

### Step 4: Deploy to Render

1. Go to **render.com** → Sign in
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect account"** → Connect GitHub
4. Select your `edumentor-mvp` repo
5. Fill settings (same as before):
   - **Name**: `edumentor-mvp-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker routes.main:app --bind 0.0.0.0:$PORT --workers 4`
6. Click **"Create Web Service"**

**Done!** Your app is live after 2-3 minutes. Visit: `https://edumentor-mvp-api.onrender.com`

---

## Option 2: Use Python Script to Upload (Alternative)

If you prefer command-line without Git CLI, I can create a Python script that uploads files directly to GitHub using the GitHub API. Run:

```powershell
python .\scripts\upload_to_github.py
```

You'll need:
- GitHub username
- Personal Access Token (create at github.com/settings/tokens)
- Repository name

---

## Recommendation

**Use Option 1 (GitHub Web UI)** — it's the fastest and requires no additional software. Just drag-and-drop files in your browser and click "Create repository".

Takes about 5 minutes total.
