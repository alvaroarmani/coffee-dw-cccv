.PHONY: help up down stop ps logs logs-postgres logs-pgadmin test

help:
	@echo "Comandos disponíveis:"
	@echo "  make up              Sobe os containers Docker"
	@echo "  make down            Derruba os containers Docker"
	@echo "  make stop            Para os containers sem remover"
	@echo "  make ps              Lista os containers"
	@echo "  make logs            Mostra logs de todos os serviços"
	@echo "  make logs-postgres   Mostra logs do PostgreSQL"
	@echo "  make logs-pgadmin    Mostra logs do pgAdmin"
	@echo "  make test            Roda os testes Python"

up:
	docker compose up -d

down:
	docker compose down

stop:
	docker compose stop

ps:
	docker compose ps

logs:
	docker compose logs

logs-postgres:
	docker compose logs postgres

logs-pgadmin:
	docker compose logs pgadmin

test:
	pytest