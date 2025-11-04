# Document Distance (AI Engineering concepts)


In the interest of time, do not implement authentication. Focus on the algorithms + deployment.
You will find the API logic has been placed in the `api_views.py` module (no need to rewrite it)

# Document Distance (AI Engineering concepts)

This project implements a small Document Distance API. The API logic is in `distance/api_views.py` and the algorithms live in `distance/algo.py`.

## Checklist (progress)

- [x] Implement algorithms in `distance/algo.py`
    - `text_to_list(text)`
    - `get_frequencies(payload)`
    - `calculate_similarity_score(freq_dict1, freq_dict2)`
- [x] Add unit tests in `distance/tests.py` (tokenization, frequencies, similarity)
- [ ] Verify API views and run locally
    - `python manage.py test`
    - `python manage.py runserver` and exercise endpoints
- [ ] Prepare Render deployment (no DB)
    - `Procfile` and `render.yaml` added
    - add `gunicorn` to `requirements.txt`
- [ ] Add GitHub Actions CI
    - `.github/workflows/ci.yml` (created)

## Quick start (local)

1. Create & activate a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run tests:

```bash
python manage.py test
```

3. Run the dev server:

```bash
python manage.py runserver
```

API endpoints (under `/api/`):
- `POST /api/text-to-list/` -> payload `{ "text": "..." }` returns token list
- `POST /api/get-frequencies/` -> payload `{ "payload": [ ... ] }` returns frequency dict

## Deploy to Render (instructions)

1. Push repository to GitHub.
2. In Render, create a new Web Service and connect to the repo.
3. Build command: `pip install -r requirements.txt` (already in `render.yaml`).
4. Start command: `gunicorn project.wsgi --log-file -` (Procfile included).
5. Do not add a managed database.

## CI

A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run tests on push and pull requests.

## Notes

- `text_to_list` currently follows the project's unit tests (punctuation merged with the following word). If you'd prefer different tokenization, update `distance/algo.py` and tests.
- Frequency dictionary keys are strings to ensure JSON-serializable responses.

---

If you want me to push these changes to a GitHub remote from this environment, tell me and I'll attempt to `git push`. If push isn't possible due to missing remote/credentials, I'll provide exact commands and a short checklist to push from your machine.