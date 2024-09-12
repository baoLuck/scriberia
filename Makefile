include .env

.PHONY:  build up down generate up-client up-server up-test clean-docs-cache \
		lint venv inside-container configure-packages

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile \
	| awk 'BEGIN{FS=":.*## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	poetry install

lint: ## Run linters
	toml-sort --in-place pyproject.toml --no-sort-tables --sort-table-keys
	pre-commit run --all-files
