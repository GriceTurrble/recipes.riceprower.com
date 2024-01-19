JEKYLL_ENV?=development
SITE_DIR=_site
CONFIG_YML=_config.yml
ifneq ($(JEKYLL_ENV),production)
	CONFIG_YML=_config.yml,_config_dev.yml
endif
export ALGOLIA_APPLICATION_ID?=TM5MJ9QNSU
export ALGOLIA_INDEX?=dev_recipes_riceprower_com

.PHONY: install build serve_site serve_static test clean clear_and_push


.PHONY: install_gems
install_gems:
	@echo ">> Installing Ruby gems..."
	@gem install jekyll bundle
	@bundle install


.PHONY: install_node_modules
install_node_modules:
	@echo ">> Installing Node dependencies..."
	@cd js_tools && \
		npm ci


install: install_gems install_node_modules


.PHONY: build_static
build_static:
	@echo ">> Building static assets (via Node)..."
	@cd js_tools && \
		npm run build


.PHONY: build_site
build_site:
	@echo ">> Building jekyll site..."
	@bundle exec jekyll build \
		--config=$(CONFIG_YML) \
		--destination=$(SITE_DIR)


build: build_static build_site


serve_site:
	@echo ">> Serving jekyll site locally (with rebuilds)..."
	@echo ">> Using CONFIG=$(CONFIG_YML)"
	@bundle exec jekyll serve \
		--config=$(CONFIG_YML)


serve_static:
	@echo ">> Serving Node assets locally (with rebuilds)..."
	@cd js_tools && \
		npm run start


test:
	@echo ">> Running tests..."
	@bundle exec htmlproofer \
		--disable-external \
		--allow_hash_href \
		$(SITE_DIR)


clean:
	@echo ">> Cleaning up Jekyll generated files..."
	@bundle exec jekyll clean \
		--config=$(CONFIG_YML)


.PHONY: push_search_records
# Refer here for env variable details:
# https://community.algolia.com/jekyll-algolia/commandline.html#environment-variables
# - In DEV (development), the overrides in _config_dev.yml should take precedence.
#   Further, the file `_algolia_api_key` can be used locally to set the push key for DEV.
# - In PROD (production), the env variable for ALGOLIA_API_KEY should be used with a secret in the CI.
# Note that the push keys for DEV and PROD are distinct for this project:
# you should NOT be using a shared admin key for both indices.
push_search_records:
	@bundle exec jekyll algolia \
		--config=$(CONFIG_YML) \
		--force-settings

.PHONY: clear_search_records
clear_search_records:
	@bundle exec ruby scripts/clear_algolia_index.rb

clear_and_push: clear_search_records push_search_records

.PHONY: rundocs deps
deps:
	poetry install

rundocs: deps
	@echo ">> Serving docs locally using 'poetry run mkdocs serve'..."
	@poetry run mkdocs serve
