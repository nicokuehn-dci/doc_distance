#!/usr/bin/env bash
# Simple smoke test script for the deployed service.
# Usage: ./scripts/smoke_test.sh https://your-service.onrender.com

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 https://your-service.onrender.com"
  exit 2
fi

BASE_URL="$1"

echo "Running smoke tests against: $BASE_URL"

run() {
  local name="$1" method="$2" path="$3" data="$4"
  echo
  echo "== $name =="
  echo "URL: $BASE_URL$path"
  http_code=$(curl -s -w "%{http_code}" -o /tmp/resp.txt -X "$method" "$BASE_URL$path" \
    -H "Content-Type: application/json" -d "$data")
  echo "HTTP status: $http_code"
  echo "Response body:" && cat /tmp/resp.txt || true
  if [ "$http_code" -ne 200 ]; then
    echo "-> $name FAILED (status $http_code)"
  else
    echo "-> $name OK"
  fi
}

run "Text to list" "POST" "/api/text-to-list/" '{"text":"Hello world, you are awesome"}'
run "Get frequencies" "POST" "/api/get-frequencies/" '{"payload":["h","e","l","l","o"]}'

rm -f /tmp/resp.txt

echo
echo "Done."
