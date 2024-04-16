# Rice-Prower Family Recipes

A collection of recipes made in the Rice-Prower home, and associated nerdy tools.

## Installation

**Prerequisites**

- Install **Node+**
- Install **Poetry for Python**

This project uses **Make** for all steps.

- If you are on Windows, install Make using [Chocolatey](https://chocolatey.org/):

  ```powershell
  choco install make
  ```

To get started:

1. Run `make deps` to install dependencies.
2. Open _two (2) terminal windows_, then:

   1. run `make run_static` to build and auto-rebuild static assets;
   2. run `make run_site` to build and auto-rebuild the site content.

3. Open your browser to `http://localhost:8000` to view the running site.

That's it! Make changes as you see fit while these two processes are running, and you'll see those changes live after refreshes.
