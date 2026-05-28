#!/bin/sh
set -eu

wait_for_tcp() {
  name="$1"
  host="$2"
  port="$3"

  echo "Waiting for $name at $host:$port..."
  python - "$host" "$port" <<'PY'
import socket
import sys
import time

host = sys.argv[1]
port = int(sys.argv[2])
deadline = time.time() + 60

while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=2):
            sys.exit(0)
    except OSError:
        time.sleep(1)

print(f"Timed out waiting for {host}:{port}", file=sys.stderr)
sys.exit(1)
PY
}

if [ "${WAIT_FOR_POSTGRES:-1}" = "1" ]; then
  wait_for_tcp "PostgreSQL" "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"
fi

if [ "${WAIT_FOR_RUSTFS:-1}" = "1" ]; then
  wait_for_tcp "RustFS" "${RUSTFS_HOST:-rustfs}" "${RUSTFS_PORT:-9000}"
fi

if [ "${API_RELOAD:-false}" = "true" ] || [ "${API_RELOAD:-false}" = "1" ]; then
  exec uvicorn main:app --host 0.0.0.0 --port "${API_CONTAINER_PORT:-8000}" --reload
fi

exec uvicorn main:app --host 0.0.0.0 --port "${API_CONTAINER_PORT:-8000}"
