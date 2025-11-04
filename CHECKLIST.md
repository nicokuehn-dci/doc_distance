# Document Distance — Checklist

This file is generated from `README.md` and includes a short "Doing" section to show current progress.

## Checklist

- [x] Implement algorithms in `distance/algo.py`
  - text_to_list(text)
  - get_frequencies(payload)
  - calculate_similarity_score(freq_dict1, freq_dict2)
- [ ] Add unit tests in `distance/tests.py` (tokenization, frequencies, similarity, edge cases)
- [ ] Verify API views and run locally
  - `python manage.py test`
  - `python manage.py runserver` and exercise endpoints
- [ ] Prepare Render deployment (no DB)
  - Add `Procfile` or `render.yaml`
  - Ensure `requirements.txt` includes `gunicorn` if using it
- [ ] Add GitHub Actions CI (optional)
  - `.github/workflows/ci.yml` to run tests on push/PR

## Quick status
- Tests currently pass locally after implementing algorithms.

## Doing (current focus)
- In progress: Add unit tests in `distance/tests.py` — write tests for:
  - `text_to_list` tokenization behaviors (punctuation merging vs separated)
  - `get_frequencies` behavior for lists and strings
  - `calculate_similarity_score` (identical -> 1.0, disjoint -> 0.0, edge cases)
- Next up after tests: Verify API views (exercise endpoints locally with `runserver`) and then prepare deployment files for Render.

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
