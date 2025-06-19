#!/bin/bash
set -e

# 載入 .env 檔案（假設與此 script 同目錄，或手動改路徑）
ENV_FILE="$(dirname "$0")/.env"

if [ -f "$ENV_FILE" ]; then
  echo "📥 Loading environment variables from $ENV_FILE"
  source "$ENV_FILE"
else
  echo "❌ .env file not found at $ENV_FILE"
  exit 1
fi

# 檢查變數
: "${POSTGRES_USER:?Missing POSTGRES_USER}"
: "${LINEBOT_DB:?Missing LINEBOT_DB}"
: "${LINEBOT_USER:?Missing LINEBOT_USER}"
: "${LINEBOT_PASS:?Missing LINEBOT_PASS}"

echo "🚀 Creating DB: $LINEBOT_DB, user: $LINEBOT_USER"

psql -U "$POSTGRES_USER" -d postgres <<-EOSQL
  CREATE DATABASE $LINEBOT_DB;
  CREATE USER $LINEBOT_USER WITH ENCRYPTED PASSWORD '$LINEBOT_PASS';
  GRANT ALL PRIVILEGES ON DATABASE $LINEBOT_DB TO $LINEBOT_USER;
EOSQL

echo "✅ Done."
