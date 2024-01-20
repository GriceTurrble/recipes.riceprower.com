.DEFAULT_GOAL := help
SITE_DIR := site## Directory to build site content to

.PHONY: deps build test run_static run_site help

.PHONY: deps_static
deps_static:## `npm ci` from `js_tools`; install Node dependencies
	@echo ">> Installing Node dependencies..."
	@cd js_tools && \
		npm ci

.PHONY: deps_poetry
deps_poetry:## `poetry install`; install Python deps using Poetry
	poetry install

deps:## shorthand for `deps_static` and `deps_poetry`
deps: deps_static deps_poetry

.PHONY: build_static
build_static:## `npm run build`; builds Node assets
	@echo ">> Building static assets (via Node)..."
	@cd js_tools && \
		npm run build

.PHONY: build_site
build_site:## `mkdocs build`; builds the site to SITE_DIR location (default 'site')
	@echo ">> Building site content (via Poetry)..."
	@poetry run mkdocs build -d $(SITE_DIR)

build:## shorthand for `build_static` then `build_site`
build: build_static build_site

run_static:## `npm run start` from `js_tools`; live-reloading Node assets builds. Calls `deps_static` first
run_static: deps_static
	@echo ">> Serving Node assets locally (with rebuilds)..."
	@cd js_tools && \
		npm run start

run_site:## `mkdocs serve`; live-reloading MkDocs build
run_site: deps_poetry
	@echo ">> Serving docs locally using 'poetry run mkdocs serve'..."
	@poetry run mkdocs serve

test:## Run tests (currently no-op)
	@echo ">> Doing nothing so far!"

help:## Show this help.
	@./help.sh "Makefile"

# @fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
