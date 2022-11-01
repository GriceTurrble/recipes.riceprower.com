# Rice-Prower Family Recipes

A collection of recipes made in the Rice-Prower home and associated nerdy tools.

## Installation

**Prerequisites**

- Install **Ruby**. Follow [jekyll prerequisites docs](https://jekyllrb.com/docs/installation/).
- Install **Node 16+**.

This project uses **Make** for all steps.

- If you are on Windows, install Make using [Chocolatey](https://chocolatey.org/):

  ```powershell
  choco install make
  ```

To get started:

1. Run `make install` to install dependencies.
2. Run `make build` to build the site and static assets the first time.
3. Open *two (2) terminal windows*, then:

   1. run `make serve_static` to build and auto-rebuild static assets;
   2. run `make serve_site` to build and auto-rebuild the site content.

4. Open your browser to `http://localhost:4000` to view the running site.

That's it! Make changes as you see fit while these two processes are running, and you'll see those changes live after refreshes.

- **Note1**: We're not fancy; there's no hot-reloading on the site itself. You'll have to actually push F5 yourself.
- **Note2**: Often when making changes, the site will rebuild immediately, followed by Tailwind generating new styles, and the site rebuilding *again* to pick up the generated styles. If things seem wonky, just refresh the browser again!

## Available Make targets

- `make install`: shorthand for installing both Ruby and Node dependencies

  This runs both of the following, which can be run independently, as well:

  - `make install_gems`: install jekyll and bundle, then run `bundle install`
  - `make install_node_modules`: run `npm ci` for Node dependencies within the [js_tools](js_tools/) directory.

- `make build`: shorthand for building the static assets, followed by the site content.

  **Order is important**. The static assets from Node must be built first, so that the site build can pick up those files.

  The following commands are run in sequence (and can be run independently):

  - `make build_static`: Runs `npm run build` for a production version of our static assets, which are generated and placed in `static/` in the repo root.
  - `make build_site`: Runs `bundle exec jekyll build` to generate the site in `_site/` directory, ready for production deployment.

- `make serve_site`: serve the site locally (at `http://localhost:4000`) with automatic rebuilds.
- `make serve_static`: builds static assets and watches for changes to both the source files and the site source files, auto-rebuilding static assets (such as Tailwind).
- `make test`: run tests on the site content, specifically HTMLProofer to check for common HTML issues in the generated content.
