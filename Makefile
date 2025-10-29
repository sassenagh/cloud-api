ENV ?= dev

GREEN := \033[0;32m
YELLOW := \033[1;33m
RESET := \033[0m

up:
	@echo "$(YELLOW)Starting environment: $(ENV)...$(RESET)"
	@ENV=$(ENV) docker-compose up -d --build
	@echo "$(GREEN)Services are up and running!$(RESET)"

down:
	@echo "$(YELLOW)Stopping containers...$(RESET)"
	@docker-compose down
	@echo "$(GREEN)Environment stopped.$(RESET)"

build:
	@echo "$(YELLOW)Building Docker images for $(ENV)...$(RESET)"
	@ENV=$(ENV) docker-compose build
	@echo "$(GREEN)Build completed.$(RESET)"

logs:
	@docker-compose logs -f

ps:
	@docker-compose ps

restart: down up
