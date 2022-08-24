CONFIG_YML=_config.yml
SITE_DIR=_site

.PHONY: install_gems install_node_modules install build_static build_site build serve_site serve_static test

# Needed locally, but not in the CI/CD workflow.
# `actions/setup-ruby` does that for us.
install_gems:
	gem install jekyll bundle
	bundle install

install_node_modules:
	@cd js_tools; \
	npm ci

install: install_gems install_node_modules

build_static:
	@cd js_tools; \
	npm run build

build_site:
	bundle exec jekyll build --config "$(CONFIG_YML)" --destination "$(SITE_DIR)"

build: build_static build_site

serve_site:
	bundle exec jekyll serve

serve_static:
	@cd js_tools; \
	npm run start

test:
	bundle exec htmlproofer --disable-external --allow_hash_href "$(SITE_DIR)"
