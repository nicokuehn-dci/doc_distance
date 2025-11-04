#!/usr/bin/env bash
# Wrapper to start gunicorn while sanitizing WEB_CONCURRENCY.
# This prevents startup failures when WEB_CONCURRENCY is set to a non-numeric
# value (for example, when a secret or token is accidentally stored there).

set -euo pipefail

# Default workers if WEB_CONCURRENCY is missing or invalid
DEFAULT_WORKERS=1

raw=${WEB_CONCURRENCY-}

if [[ -z "$raw" ]]; then
  WORKERS=$DEFAULT_WORKERS
else
  # Keep only digits
  if [[ "$raw" =~ ^[0-9]+$ ]]; then
    WORKERS=$raw
  else
    echo "Warning: WEB_CONCURRENCY='$raw' is not numeric; falling back to $DEFAULT_WORKERS" 1>&2
    WORKERS=$DEFAULT_WORKERS
  fi
fi

export WEB_CONCURRENCY=$WORKERS

echo "Resolved WEB_CONCURRENCY=$WEB_CONCURRENCY" 1>&2

# If DRY_RUN=1, print resolved value and exit without starting gunicorn.
if [[ "${DRY_RUN-0}" == "1" || "${DRY_RUN-}" == "true" || "${DRY_RUN-}" == "yes" ]]; then
  echo "DRY_RUN enabled — not starting gunicorn" 1>&2
  exit 0
fi

# Use exec so the shell is replaced by gunicorn (proper signal handling)
exec gunicorn project.wsgi --log-file - -w "$WEB_CONCURRENCY"
