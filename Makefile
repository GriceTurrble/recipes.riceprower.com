### Help doc stuff
SERVICE := recipes.riceprower.com
SERVICE_SHORT_DESCRIPTION := A collection of recipes made in the Rice-Prower home, and associated nerdy tools.

### Variables
SITE_DIR := site

### Commands
.PHONY: lock
lock: ## `poetry lock`
	poetry lock


.PHONY: deps_static
deps_static: ## `npm ci` from `js_tools`; install Node dependencies
	@echo ">> Installing Node dependencies..."
	@cd js_tools && \
		npm ci


.PHONY: deps_poetry
deps_poetry: ## `poetry install`; install Python deps using Poetry
	poetry install


.PHONY: deps
deps: ## shorthand for `deps_static` and `deps_poetry`
deps: deps_static deps_poetry


.PHONY: build_static
build_static:## `npm run build`; builds Node assets
	@echo ">> Building static assets (via Node)..."
	@cd js_tools && \
		npm run build


.PHONY: build_site
build_site: ## `mkdocs build`; builds the site to SITE_DIR location (default 'site')
	@echo ">> Building site content (via Poetry)..."
	@poetry run mkdocs build -d $(SITE_DIR)


.PHONY: build
build: ## shorthand for `build_static` then `build_site`
build: build_static build_site


.PHONY: run_static
run_static: ## `npm run start` from `js_tools`; live-reloading Node assets builds. Calls `deps_static` first
run_static: deps_static
	@echo ">> Serving Node assets locally (with rebuilds)..."
	@cd js_tools && \
		npm run start


.PHONY: run_site
run_site: ## `mkdocs serve`; live-reloading MkDocs build
run_site: deps_poetry
	@echo ">> Serving docs locally using 'poetry run mkdocs serve'..."
	@poetry run mkdocs serve


.PHONY: test
test: ## Run tests (currently no-op)
	@echo ">> Doing nothing so far!"


.DEFAULT_GOAL := help
.PHONY: help
help: ## Display this help screen
	@echo "\033[1m$(SERVICE)\033[0m"
	@echo "  $(SERVICE_SHORT_DESCRIPTION)\n"
	@echo "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'
