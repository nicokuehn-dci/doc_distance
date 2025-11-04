# Deploying to Render (CI)

This project includes a GitHub Actions workflow that triggers a Render deploy when code is pushed to `main`, and runs smoke tests against the live service after a successful deploy.

## What the workflow does
- On push to `main` it calls the Render API to create a deploy for the service id you configure.
- It polls the deploy until it finishes.
- After a successful deploy it runs two smoke tests against the live URL:
  - POST /api/text-to-list/
  - POST /api/get-frequencies/

If the smoke tests fail the workflow job exits non-zero and the GitHub Action run is marked as failed.

## Setup (GitHub repository secrets)
Before the workflow can run you must add two repository secrets in GitHub:

- `RENDER_API_KEY` — a Render API key with access to your services. Create one in the Render dashboard: Account → API Keys.
- `RENDER_SERVICE_ID` — the Render service id for this repository (e.g. `srv-d44v0uh5pdvs73c1gki0`).

How to add secrets:
1. Open your GitHub repository → Settings → Secrets → Actions → New repository secret.
2. Add `RENDER_API_KEY` and paste the API key value.
3. Add `RENDER_SERVICE_ID` and paste the service id value.

Important: Treat the API key as a secret. If you ever expose or paste it in public, revoke and recreate it in Render immediately.

## Local verification and manual deploy
If you prefer to trigger deploys manually from your machine (instead of via the workflow), you can use the Render API or the Render CLI.

Manual API example (local):
```bash
export RENDER_API_KEY="rnd_..."
SERVICE_ID="srv-..."
# Trigger deploy
curl -X POST "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Content-Type: application/json" -d '{}'
```

After deploy completes, the workflow’s smoke tests expect the live site to respond to the two endpoints above.

## Troubleshooting
- If the build succeeds but the deploy fails with a `ValueError` about `WEB_CONCURRENCY`, ensure:
  - The Render Start Command is `./scripts/start_gunicorn.sh` (the wrapper sanitizes `WEB_CONCURRENCY`), or
  - The `WEB_CONCURRENCY` env var in Render is set to an integer (e.g. `2`) or removed.

- If the smoke tests fail, inspect the deploy logs in the Render dashboard and paste any stack trace into the issue/PR for debugging.

---

If you'd like, I can add the smoke-test job to also post results to Slack or annotate the PR with the output — tell me which integration you prefer and I will add it.