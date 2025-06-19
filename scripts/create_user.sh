#!/usr/bin/env bash
set -euo pipefail

# 1) 找到專案根目錄的 .env
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env not found at $ENV_FILE" >&2
  exit 1
fi

# 2) 讀入所有變數並 export
set -o allexport
# shellcheck disable=SC1090
source "$ENV_FILE"
set +o allexport

# 3) 定義 container name，若 .env 裡沒給就用 APP_NAME 來組
: "${POSTGRES_CONTAINER_NAME:=${APP_NAME}_postgres}"

echo "→ 執行 Container: $POSTGRES_CONTAINER_NAME"

# 4) 最後呼叫 docker exec
docker exec -i "$POSTGRES_CONTAINER_NAME" psql \
  -U "$POSTGRES_ADMIN" \
  -d "$DB_NAME" <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles
    WHERE rolname = '$POSTGRES_USER'
  ) THEN
    CREATE ROLE $POSTGRES_USER LOGIN PASSWORD '$POSTGRES_USER_PASS';
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${POSTGRES_USER};
    RAISE NOTICE 'Role \"$POSTGRES_USER\" created.';
  ELSE
    RAISE NOTICE 'Role \"$POSTGRES_USER\" already exists. Skipping.';
  END IF;
END
\$\$;
SQL
