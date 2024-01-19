from typing import Any
from pathlib import Path

import mkdocs_gen_files
import frontmatter


DIR = Path(__file__).parent.parent
SRC = DIR / "recipes"
OUT = "recipes"


def print_directions(data: dict[str, Any], file):
    """Generates ordered list of Directions."""
    print("### Directions", file=file)
    print('<div class="recipe-directions" markdown>\n', file=file)
    for direction in data["directions"]:
        print(f"1. {direction.strip()}", file=file)
    print("\n</div>\n", file=file)


def print_ingredients(data: dict[str, Any], file):
    """Generates unordered list of Ingredients."""
    print("### Ingredients", file=file)
    print('<div class="recipe-ingredients" markdown>\n', file=file)
    for ingredient in data["ingredients"]:
        print(f"- [ ] {ingredient.strip()}", file=file)
    print("\n</div>\n", file=file)


for file in SRC.rglob("*.md"):
    contents = file.read_text()
    data = frontmatter.loads(contents)

    doc_path = file.relative_to(SRC).with_suffix(".md")
    full_doc_path = Path(OUT, doc_path)

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print(contents, file=fd)

        print('<div class="recipe-contents" markdown>\n', file=fd)

        print_ingredients(data, file=fd)
        print_directions(data, file=fd)

        print('</div>\n', file=fd)
