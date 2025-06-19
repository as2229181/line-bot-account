# Makefile

MAKEFLAGS += --silent

# 預設為 .env，如果 make init-db ENV=.env.dev 就改用 .env.dev
ENV ?= .env

# 讀取 .env 檔並 export 所有變數
include $(ENV)
export $(shell sed 's/=.*//' $(ENV))

CONTAINER_NAME := linebot-db

.PHONY: all

up-postgres:
	@echo "Create and Update PostgreSQL $(POSTGRES_CONTAINER_NAME)"
	@docker compose build

init-db:
	@echo " Using env file: $(ENV)"
	@echo " Initializing PostgreSQL in container '$(CONTAINER_NAME)'..."
	@docker exec -i $(CONTAINER_NAME) psql -U $(POSTGRES_USER) -d postgres \
		-c "CREATE DATABASE $(LINEBOT_DB);" 2>/dev/null || echo " Database '$(LINEBOT_DB)' may already exist"
	@docker exec -i $(CONTAINER_NAME) psql -U $(POSTGRES_USER) -d postgres \
		-c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$(LINEBOT_USER)') THEN CREATE USER $(LINEBOT_USER) WITH ENCRYPTED PASSWORD '$(LINEBOT_PASS)'; END IF; END \$\$;" || true
	@docker exec -i $(CONTAINER_NAME) psql -U $(POSTGRES_USER) -d postgres \
		-c "GRANT ALL PRIVILEGES ON DATABASE $(LINEBOT_DB) TO $(LINEBOT_USER);"
	@echo "DB '$(LINEBOT_DB)' and user '$(LINEBOT_USER)' initialized."
