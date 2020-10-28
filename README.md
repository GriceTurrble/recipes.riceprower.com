# HomeTools

A collection of tools used in the Rice-Prower home on their server and stuff.

## Getting started

1. Install [Python](https://python.org) (latest is 3.9).
2. Install [Visual Studio Code](https://code.visualstudio.com/).
3. Clone this repo somewhere on your machine.
4. Using PowerShell, navigate to the root directory of the project, then create a **Python virtual environment**, or **venv**.
    - I recommend doing so with this command: `python -m venv .venv --prompt hometools`
5. Activate the venv by running command: `.venv/Scripts/Activate.ps1`
    - The beginning of the command prompt should read `(hometools)`. If it doesn't, back up and ask for assistance from G.
6. Upgrade `pip` in the venv: `python -m pip install --upgrade pip`
7. Install the project dev requirements: `pip install -r requirements-dev.txt`
8. "cd" into the project source directory: `cd hometools`
9. Generate a `.env` file containing local environment settings: `python generate_env.py`
    - This is necessary to get the local database settings straightened out.
10. "Migrate" the database, so it builds its schema: `python manage.py migrate`
11. Create your superuser account: `python manage.py createsuperuser`
    - Follow the prompts to enter your details. Username, email, and password
    - The password can be as simple as you want it, like "what" or "something". It will warn you about using an unsafe password, but you can type "y" and hit Enter to acknowledge that, as I recall.
12. Start running the app: `python manage.py runserver`
13. Open your browser to http://localhost:8000, and you should see the home page come up.

### Development tooling

Talk to G to have him set up VSCode with some extra tools to run the project, including the following stuff.

#### .vscode/launch.json

```json
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
      "program": "${workspaceFolder}\\hometools\\manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

#### Extensions

- "Django" [batisteo.vscode-django]
- "Prettier - Code formatter" [esbenp.prettier-vscode]
- "GitLens — Git supercharged" [eamodio.gitlens]

#### Settings

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
  "terminal.integrated.cwd": "${workspaceFolder}\\hometools",
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true
}
```

*I can explain everything going on if you like, but somehow I doubt you'll take me up on the offer.*

## Applications

### Invoices

Builds invoices and timesheets for contract projects.

### Recipes

A collection of recipes the family likes.
