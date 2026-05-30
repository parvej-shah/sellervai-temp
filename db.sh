#!/bin/sh
set -eu

ALEMBIC_CFG="alembic.ini"

usage() {
  cat <<EOF
Usage: $0 <command> [options]

Commands:
  reset    Wipe the database and reapply migrations (destructive)
  seed     Run the seed script: scripts/seed.py
  migrate  Run alembic upgrade head

Options:
  --yes    skip confirmation for destructive operations (or set FORCE=1)

Environment:
  DATABASE_URL   required (or put it in .env)

Examples:
  # reset DB (requires --yes or FORCE=1)
  sh db.sh reset --yes

  # reset DB and seed
  FORCE=1 sh db.sh reset --yes && sh db.sh seed

  # run migrations
  sh db.sh migrate
EOF
  exit 1
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ] || [ -z "${1:-}" ]; then
  usage
fi

# Load .env if present
if [ -f ".env" ]; then
  echo "Loading environment from .env"
  # Use Python's dotenv parser so malformed lines in .env do not break the shell.
  DOTENV_VARS=$(python3 - <<'PY'
from pathlib import Path
import shlex

path = Path('.env')
for raw_line in path.read_text().splitlines():
    line = raw_line.strip()
    if not line or line.startswith('#'):
        continue
    if line.startswith('export '):
        line = line[len('export '):].strip()
    if '=' not in line:
        continue
    key, value = line.split('=', 1)
    key = key.strip()
    value = value.strip()
    if not key:
        continue
    # Keep quoted values as shell-safe assignments.
    print(f"{key}={shlex.quote(value)}")
PY
)
  if [ -n "$DOTENV_VARS" ]; then
    eval "$DOTENV_VARS"
  fi
fi

CMD="$1"
shift || true

ensure_database_url() {
  if [ -z "${DATABASE_URL:-}" ]; then
    echo "ERROR: DATABASE_URL is not set. Export it or set it in .env and re-run."
    exit 2
  fi
}

run_seed() {
  if [ -f "scripts/seed.py" ]; then
    echo "Running seed script..."
    python3 scripts/seed.py
  else
    echo "No seed script found at scripts/seed.py"
  fi
}

case "$CMD" in
  reset)
    ensure_database_url

    # require explicit confirmation to avoid accidental data loss
    if [ "${FORCE:-}" != "1" ] && [ "${1:-}" != "--yes" ]; then
      echo "This will permanently delete all data in the database at: ${DATABASE_URL}"
      echo "Re-run with --yes or set FORCE=1 to proceed."
      exit 3
    fi

    echo "Resetting database at: ${DATABASE_URL}"

    case "$DATABASE_URL" in
      sqlite:*)
      # handle sqlite URLs like sqlite:///./db.sqlite3 or sqlite:////absolute/path
      SQLITE_PATH="${DATABASE_URL#sqlite:///}"
      SQLITE_PATH="${SQLITE_PATH#file:}"
      if [ "$SQLITE_PATH" = ":memory:" ]; then
        echo "In-memory sqlite, nothing to remove."
      else
        if [ -f "$SQLITE_PATH" ]; then
          echo "Removing sqlite file: $SQLITE_PATH"
          rm -f "$SQLITE_PATH"
        else
          echo "Could not find sqlite file to remove: $SQLITE_PATH"
        fi
      fi
      ;;
      postgresql*|postgres*)
      # Transform SQLAlchemy URL that may contain +asyncpg into a driver URL psycopg2 can open.
      CLEAN_URL=$(printf '%s' "$DATABASE_URL" | sed 's/+asyncpg//')
      echo "Dropping and recreating public schema via Python..."
      python3 - "$CLEAN_URL" <<'PY'
import sys
import psycopg2

dsn = sys.argv[1]
conn = psycopg2.connect(dsn)
conn.autocommit = True
try:
    with conn.cursor() as cur:
        cur.execute("DROP OWNED BY CURRENT_USER CASCADE")
        cur.execute("DROP TYPE IF EXISTS public.webhookstatus CASCADE")
        cur.execute("DROP TYPE IF EXISTS public.servicestatus CASCADE")
        cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
        cur.execute("CREATE SCHEMA public")
finally:
    conn.close()
PY
      ;;
      *)
      echo "Unknown/unsupported DB type in DATABASE_URL. Attempting alembic downgrade base."
      alembic -c "$ALEMBIC_CFG" downgrade base
      ;;
    esac

    echo "Applying migrations..."
    alembic -c "$ALEMBIC_CFG" upgrade head

    # optionally seed if user requested
    if [ "${1:-}" = "--seed" ] || [ "${SEED:-}" = "1" ]; then
      run_seed
    fi

    echo "Reset complete."
    ;;

  seed)
    ensure_database_url
    run_seed
    ;;

  migrate)
    ensure_database_url
    echo "Running alembic upgrade head..."
    alembic -c "$ALEMBIC_CFG" upgrade head
    ;;

  *)
    usage
    ;;
esac
