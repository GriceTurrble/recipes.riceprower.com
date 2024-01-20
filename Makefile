SITE_DIR?=site

.PHONY: deps build

.PHONY: deps_static
deps_static:
	@echo ">> Installing Node dependencies..."
	@cd js_tools && \
		npm ci

.PHONY: deps_poetry
deps_poetry:
	poetry install

deps: deps_static deps_poetry

.PHONY: build_static
build_static:
	@echo ">> Building static assets (via Node)..."
	@cd js_tools && \
		npm run build

.PHONY: build_site
build_site:
	@echo ">> Building site content (via Poetry)..."
	@poetry run mkdocs build -d $(SITE_DIR)

build: build_static build_site

.PHONY: serve_static
serve_static:
	@echo ">> Serving Node assets locally (with rebuilds)..."
	@cd js_tools && \
		npm run start

.PHONY: run_static
run_static: deps_static serve_static

.PHONY: run_site
run_site: deps_poetry
	@echo ">> Serving docs locally using 'poetry run mkdocs serve'..."
	@poetry run mkdocs serve
