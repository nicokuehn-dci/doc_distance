# Deploying Document Distance API to Render

This guide walks through deploying the project to Render's Web Service (Python) using the repository already pushed to GitHub.

Prerequisites
- You have a Git provider account (GitHub/GitLab) and the repo is pushed there.
- Your `requirements.txt` contains `gunicorn` (this project already includes it).
- `Procfile` or `render.yaml` are present in the repo (this project includes both).

Quick summary of commands used by Render
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn project.wsgi --log-file -`

Step-by-step (Render web UI)
1. Sign in to Render (https://render.com) and go to your Dashboard.
2. Click "New" → "Web Service".
3. Connect your Git provider and select the repository and branch (e.g., `main`).
4. For Environment, choose `Python`.
5. (Optional) Use the default region and plan. Free plan is OK for basic testing.
6. Build settings:
   - Build Command: (leave default) `pip install -r requirements.txt` (or keep as in `render.yaml`).
   - Start Command: `gunicorn project.wsgi --log-file -` (or `web: gunicorn project.wsgi --log-file -` if using Procfile).
7. Environment
   - Add environment variables:
     - `SECRET_KEY` — copy a strong secret for production.
     - `ALLOWED_HOSTS` — set to your Render service URL (or `*` for quick testing).
     - `DEBUG` — set to `False` in production; you can use `True` for early testing but avoid in prod.
     - (Optional) `DISABLE_COLLECTSTATIC=1` if you don't want Render to run collectstatic.
8. Deploy: click "Create Web Service". Render will run the build and then start the service.

Post-deploy checks & troubleshooting
- Watch the deploy logs (Render Dashboard → Service → Events/Deploys → View logs). Look for:
  - Errors during `pip install` (dependency issues). Fix by pinning correct versions in `requirements.txt`.
  - Runtime stack traces after startup — these appear in the server logs.
- Common issues & fixes:
  - "Exited with status 1" or start command not found: ensure `gunicorn` is listed in `requirements.txt` and the start command matches your Procfile.
  - `DisallowedHost` or `Invalid HTTP_HOST`: add the service host (e.g., `my-service.onrender.com`) to `ALLOWED_HOSTS` or set `ALLOWED_HOSTS=['*']` temporarily.
  - Missing `SECRET_KEY` or other env vars: set them in Render's Environment settings.
  - SQLite file permissions: by default Render's ephemeral filesystem is writable at runtime, but avoid relying on SQLite for shared/production data. For persistence, use a managed database.
  - Collectstatic failures: if DEBUG=False, Django tries to collect static files. Either set `DISABLE_COLLECTSTATIC=1` or configure `STATIC_ROOT` and ensure `collectstatic` runs successfully.

How to reproduce a failing deploy locally
1. Recreate your environment and run the same build steps locally:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
2. Start the app with Gunicorn as Render does:
```bash
.venv/bin/gunicorn project.wsgi --bind 0.0.0.0:8000 --log-file -
```
3. Tail the logs and make requests to verify behavior.

If deploy fails, capture the Render log (copy/paste or screenshot) and share it here — I can parse it and give a targeted fix.

Optional: Using Docker on Render
- If you prefer full control, add a `Dockerfile` and select "Docker" when creating the service in Render. This gives a reproducible environment.

Rollback and redeploy
- In the Render UI you can redeploy an earlier commit from the deploy history.
- To force a fresh redeploy after fixes, make a small commit and push to your repo (Render will trigger a new deploy if connected).

Notes and security
- Do not set `ALLOWED_HOSTS=['*']` or leave `DEBUG=True` in production for security reasons.
- Use environment variables for secrets and never commit them to the repo.

## Exact environment variables to set on Render
Set the following environment variables in the Render service dashboard (Service → Environment). Replace example values with real secrets.

- SECRET_KEY (string) — Django secret key. Example: `pM8...` (generate with Django's get_random_secret_key())
- DEBUG (boolean) — `True` or `False` (use `False` in production)
- ALLOWED_HOSTS (comma-separated) — e.g. `my-app.onrender.com,localhost`
- DATABASE_URL (optional) — Postgres connection string: `postgres://USER:PASSWORD@HOST:PORT/DB_NAME`
- DISABLE_COLLECTSTATIC (optional) — set to `1` to skip `collectstatic` during deploy

Email / optional settings (only if you use them):
- EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, DEFAULT_FROM_EMAIL

Storage / third-party keys (if used):
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
- THIRD_PARTY_API_KEY (example)

After setting the environment variables, trigger a new deploy (either push a commit or use Render's "Deploy Latest Commit").

---

If you want, I can add this `DEPLOY.md` to the repo and commit it for you, or I can also revert the punctuation-merge tokenization in `distance/algo.py` and update tests accordingly. Tell me which you'd like me to do next (commit DEPLOY.md here, revert tokenization, or both).