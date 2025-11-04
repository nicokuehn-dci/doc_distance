# Document Distance — Checklist

This file is generated from `README.md` and includes a short "Doing" section to show current progress.

## Checklist

- [x] Implement algorithms in `distance/algo.py`
  - text_to_list(text)
  - get_frequencies(payload)
  - calculate_similarity_score(freq_dict1, freq_dict2)
 - [x] Add unit tests in `distance/tests.py` (tokenization, frequencies, similarity, edge cases)
 - [x] Verify API views and run locally
   - `python manage.py test` (tests passed locally)
   - `python manage.py runserver` and exercise endpoints (validated)
 - [x] Prepare Render deployment (no DB)
   - `Procfile` and `render.yaml` added
   - `gunicorn` added to `requirements.txt`
 - [x] Add GitHub Actions CI (optional)
   - `.github/workflows/ci.yml` added to run tests on push/PR

## Quick status
- All checklist items have been completed locally and pushed to the repository.
- Tests: 6 tests ran locally and passed (OK).
- Dev server: started locally and API endpoints validated.

## Doing (current focus)
- Repository: changes committed and pushed to `origin/main` on GitHub.
- Next recommended steps (optional): monitor CI runs on GitHub Actions, and create a Render web service pointing to this repository to deploy.

## New: DEPLOY.md
- `DEPLOY.md` has been created with step-by-step Render UI instructions and troubleshooting tips.
- Action: I will commit and push `DEPLOY.md` to `origin/main` now so the repo contains the deploy guide.

## How to run tests locally

1. Create & activate venv, install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the Django test suite:

```bash
python manage.py test
```

3. Run the dev server and try endpoints:

```bash
python manage.py runserver
```

## Notes / Decisions
- `text_to_list` currently merges punctuation with the following word to match existing unit tests (e.g., ",you"). If you prefer punctuation as separate tokens, change `distance/algo.py` accordingly and update tests.
- Keys in frequency dictionaries are strings to ensure JSON-serializable responses.

---

If you want, I can now:
- Add the unit tests (I will update `distance/tests.py` and run `python manage.py test`).
- Prepare a `Procfile` and optional `render.yaml` for deployment.
- Add a GitHub Actions CI workflow file.

Tell me which step to do next and I'll proceed.

## Render troubleshooting checklist

If your Render deploy shows "Exited with status 1" or a runtime error, try the following checks (ordered by frequency):

1. Check build logs for dependency install failures
  - On Render: Service → Events / Deploys → View deploy logs.
  - If pip fails, ensure `requirements.txt` is valid and pinned. Re-run locally: `pip install -r requirements.txt`.

2. Ensure `gunicorn` is installed and start command matches your Procfile
  - `requirements.txt` must include `gunicorn`.
  - Start command used here: `gunicorn project.wsgi --log-file -`.

3. ALLOWED_HOSTS / DEBUG
  - In production set `DEBUG=False` and add your Render hostname to `ALLOWED_HOSTS` or set `ALLOWED_HOSTS=['*']` for quick testing (not recommended for production).

4. Missing environment variables
  - If your code reads env vars (SECRET_KEY, etc.), set them in Render (Dashboard → Environment). Missing secrets often cause startup crashes.

5. Database / migrations
  - This app doesn't need a managed DB. If you switch to one, run migrations: `python manage.py migrate`.

6. File system / static files
  - If DEBUG=False, ensure `STATIC_ROOT` is set and run `collectstatic` if needed (or disable collectstatic in Render by setting `PYTHONUNBUFFERED` or `DISABLE_COLLECTSTATIC` env var appropriately).

7. Inspect runtime logs for stack traces
  - Use the Render UI logs page to find the Python exception and stack trace, then paste it here and I can give a targeted fix.

Quick local reproduction steps

```bash
# create/activate venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run locally with gunicorn
.venv/bin/gunicorn project.wsgi --bind 127.0.0.1:8001 --log-file -

# or run Django dev server for quick checks
python manage.py runserver 127.0.0.1:8000
```

If you prefer, I can fetch your latest Render deploy logs and parse the error for you — tell me "get render logs" and paste the deploy log URL or its text output, and I'll analyze it.
