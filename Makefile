.DEFAULT_GOAL := help

SHELL := /usr/bin/env bash

project := bot

.PHONY: setup # Setup a working environment
setup:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: prepare-files # Copy '.env.example' file to '.env'
prepare-files:
	@echo Copying files...
	@cp --verbose .env.example .env
	@echo Do not forget to modify:
	@echo - .env

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	pipenv shell

.PHONY: lint # Run linter
lint:
	pipenv run pylint ${project}/

.PHONY: prepare-temp-containers
prepare-temp-containers:
	@echo Starting db container...
	@docker run -d \
		--rm \
		--pull always \
		--name ${project}_temp_db \
		--env-file .env \
		-p 5432:5432 \
		postgres:13-alpine

stop-prepared-temp-containers := echo; \
	echo Stopping db container...; \
	docker stop ${project}_temp_db

.PHONY: prepare-db
prepare-db:
	@sleep 1
	@echo Initializing database...
	@pipenv run python fill_db_with_sample_data.py

.PHONY: start # Start application (with database)
start: prepare-temp-containers prepare-db
	@trap '${stop-prepared-temp-containers}' EXIT && \
		echo Starting application... && \
		pipenv run python -m ${project}.main

.PHONY: db # Start Postgres container
db: prepare-temp-containers prepare-db
	@trap '${stop-prepared-temp-containers}' EXIT && \
		echo Press CTRL+C to stop && \
		sleep 1d

.PHONY: app # Start application (without database)
app:
	@echo Starting application...
	pipenv run python -m ${project}.main

.PHONY: requirements # Generate requirements.txt file
requirements:
	pipenv lock --requirements > requirements.txt

.PHONY: up # Start Compose services
up:
	docker-compose pull db
	docker-compose build --pull
	docker-compose up

.PHONY: down # Stop Compose services
down:
	docker-compose down

.PHONY: help # Print list of targets with descriptions
help:
	@echo; \
		for mk in $(MAKEFILE_LIST); do \
			echo \# $$mk; \
			grep '^.PHONY: .* #' $$mk \
			| sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' \
			| expand -t20; \
			echo; \
		done
