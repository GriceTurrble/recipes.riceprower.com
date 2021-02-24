# Rice-Prower Family Recipes

A collection of recipes made in the Rice-Prower home and associated nerdy tools.

## Getting started

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install [Docker](https://www.docker.com/) on your desktop.
3. Write environment files within the project root, at the same level as this README file:

   - Create a `.recipes.env` file containing the following:

     ```
     HT_SECRET_KEY=<some-random-long-string-of-characters>
     HT_TIME_ZONE=US/Eastern
     HT_ALLOWED_HOSTS=*

     # Database:
     HT_DB_ENGINE=django.db.backends.postgresql
     DB_NAME=postgres
     DB_USER=postgres
     DB_PASSWORD=postgres
     DB_HOST=db
     DB_PORT=5432
     ```

     Write whatever long string of random characters you like for `HT_SECRET_KEY`, then save the file as-is.

   - Create a `.postgres.env` file containing:

     ```
     POSTGRES_DB=postgres
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=postgres
     ```

     Note these should all match the corresponding values shown in `.recipes.env`.

     These values are all the basics used in development. These do not match production credentials (as that would be silly).

4. Start up the services using:

   ```bash
   docker-compose up -d
   ```

5. Create your superuser account within the running `web` container using:

   ```bash
   docker-compose exec web poetry run python /app/recipesite/manage.py createsuperuser
   ```

6. Open your browser to http://localhost:8008, and you should see the home page come up.

## Development tooling

Talk to G to have him set up VSCode with some extra tools to run the project, including the following stuff.

### .vscode/launch.json

```jsonc
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: Runserver",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}\\recipesite\\manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

### Extensions

- "Django" [batisteo.vscode-django]
- "Prettier - Code formatter" [esbenp.prettier-vscode]
- "GitLens — Git supercharged" [eamodio.gitlens]

### Settings

**User settings:**

```jsonc
{
  // Adjusting the settings editor so you can actually copy over these settings and not waste time.
  "workbench.settings.editor": "json",
  "workbench.settings.useSplitJSON": true,
  // Editor
  "editor.autoClosingBrackets": "never",
  "editor.renderWhitespace": "all",
  "editor.autoClosingQuotes": "never",
  "editor.autoSurround": "never",
  "editor.detectIndentation": false,
  // Files
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.associations": {
    "**/templates/*.html": "django-html",
    "**/templates/*": "django-txt",
    "**/requirements{/**,*}.{txt,in}": "pip-requirements"
  },
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/.hg": true,
    "**/CVS": true,
    "**/.DS_Store": true,
    "**/.venv/": true,
    "**/__pycache__/": true
  },
  // Language specifics
  "[html]": {
    "editor.tabSize": 2
  },
  "[django-html]": {
    "editor.tabSize": 2
  },
  "[css]": {
    "editor.tabSize": 2
  },
  "[javascript]": {
    "editor.tabSize": 2,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.tabSize": 2,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonc]": {
    "editor.tabSize": 2,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.wordWrap": "bounded",
    "editor.quickSuggestions": false,
    "editor.wordWrapColumn": 100,
    "editor.rulers": [100]
  },
  // Python
  "python.formatting.provider": "black",
  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.untrackedChanges": "separate",
  // Emmet
  "emmet.includeLanguages": {
    "django-html": "html"
  },
  // Misc
  "prettier.trailingComma": "none",
  "python.languageServer": "Pylance",
  "diffEditor.ignoreTrimWhitespace": false,
  "diffEditor.renderSideBySide": true
}
```

**Workspace settings:**

```json
{
  "terminal.integrated.cwd": "${workspaceFolder}\\recipesite",
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true
}
```

*I can explain everything going on if you like, but somehow I doubt you'll take me up on the offer.*
