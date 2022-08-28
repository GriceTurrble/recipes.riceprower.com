CONFIG_YML=_config.yml
SITE_DIR=_site
ENFORCE_HTTPS_IN_TESTS?=false

.PHONY: install_gems install_node_modules install build_static build_site build serve_site serve_static test

# Needed locally, but not in the CI/CD workflow.
# `actions/setup-ruby` does that for us.
install_gems:
	@echo ">> Installing Ruby gems..."
	@gem install jekyll bundle
	@bundle install

install_node_modules:
	@echo ">> Installing Node dependencies..."
	@cd js_tools && \
		npm ci

install: install_gems install_node_modules

build_static:
	@echo ">> Building static assets (via Node)..."
	@cd js_tools && \
		npm run build

build_site:
	@echo ">> Building jekyll site..."
	@bundle exec jekyll build \
		--config "$(CONFIG_YML)" \
		--destination "$(SITE_DIR)"

build: build_static build_site

serve_site:
	@echo ">> Serving jekyll site locally (with rebuilds)..."
	@bundle exec jekyll serve

serve_static:
	@echo ">> Serving Node assets locally (with rebuilds)..."
	@cd js_tools && \
		npm run start

test:
	@echo ">> Running tests..."
	@bundle exec htmlproofer \
		--disable-external \
		--allow_hash_href \
		--enforce-https=$(ENFORCE_HTTPS_IN_TESTS) \
		"$(SITE_DIR)"

clean:
	@echo ">> Cleaning up Jekyll generated files..."
	@bundle exec jekyll clean
