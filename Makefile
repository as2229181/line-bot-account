# Makefile

MAKEFLAGS += --silent

# 預設為 .env，如果 make init-db ENV=.env.dev 就改用 .env.dev
ENV ?= .env

# 讀取 .env 檔並 export 所有變數
include $(ENV)
export ENV
export $(shell sed 's/=.*//' $(ENV))

CONTAINER_NAME := linebot-db

.PHONY: all
up-app:
	@echo "up app service"
	@docker compose --env-file $(ENV) up app -d

down-app:
	@echo "down app service"
	@docker compose --env-file $(ENV) down app

up-postgres:
	@echo "up PostgreSQL $(POSTGRES_CONTAINER_NAME)"
	@docker compose --env-file $(ENV) up postgres -d

down-postgres:
	@echo "dwon PostgreSQL $(POSTGRES_CONTAINER_NAME)"
	@docker compose --env-file $(ENV) down postgres

postgres-shell:
	@echo "enter PostgreSQL $(POSTGRES_CONTAINER_NAME) bash shell"
	@docker compose exec -it postgres bash

init-db-path:
	@echo "Start to init db path..."
	@if [ -d $(DB_PATH)/postgres ]; then \
	echo "$(DB_PATH)/postgres already exist"; \
	else \
	    echo "create $(DB_PATH)/postgres"; \
	    mkdir -p $(DB_PATH)/postgres; \
	fi

create-db-user: up-postgres
	@if [ -z "$$(docker ps -q -f name=$(POSTGRES_CONTAINER_NAME))" ]; then \
		  echo "Container '$(POSTGRES_CONTAINER_NAME)' 未啟動！請先執行 'make up-postgres'。"; \
		  exit 1; \
		fi
	@bash $(PROJECT_SCRIPT_PATH)/create_user.sh

init-db:
	@echo "初始化資料庫遷移檔案..."
	docker-compose run --rm app_build flask db init
	docker-compose run --rm app_build flask db migrate
	docker-compose run --rm app_build flask db upgrade