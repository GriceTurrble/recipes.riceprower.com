from typing import Any
from pathlib import Path

import mkdocs_gen_files
import frontmatter


DIR = Path(__file__).parent.parent
SRC = DIR / "recipes"
OUT = "recipes"


def print_stats(data: dict[str, Any], file):
    output = []
    total_prep = data.get("prep_time", 0) + data.get("cook_time", 0)
    if (part := data.get("prep_time")) is not None:
        output.append(
            f"- :material-map-clock: **Prep** {part} minute{'s' if part != 1 else ''}"
        )
    if (part := data.get("cook_time")) is not None:
        output.append(f"- :cooking: **Cook** {part} minute{'s' if part != 1 else ''}")
    output.append(
        f"- :material-clock: **Total** {total_prep} minute{'s' if total_prep != 1 else ''}"
    )
    if (part := data.get("servings")) is not None:
        output.append(
            f"- :fork_and_knife: **{part} serving{'s' if part != 1 else ''}**"
        )

    print('<div style="display: flex; justify-content: center;" markdown>', file=file)
    img_src = data["image"]["href"]
    print(f'<div class="recipe-image"><img style="margin-top: 1rem; height: 300px;" src="{img_src}"/></div>', file=file)
    print('<div class="grid cards" markdown>\n', file=file)
    [print(x, file=file) for x in output]
    print("</div>", file=file)
    print("</div>\n", file=file)


def print_ingredients(data: dict[str, Any], file):
    """Generates unordered list of Ingredients."""
    if not data.get("ingredients"):
        # Not present or empty, skip printing
        return
    print('<div class="recipe-ingredients" markdown>\n', file=file)
    print("### Ingredients", file=file)
    for ingredient in data["ingredients"]:
        print(f"- [ ] {ingredient.strip()}", file=file)
    print("\n</div>\n", file=file)


def print_directions(data: dict[str, Any], file):
    """Generates ordered list of Directions."""
    if not data.get("directions"):
        # Not present or empty, skip printing
        return
    print('<div class="recipe-directions" markdown>\n', file=file)
    print("### Directions", file=file)
    for direction in data["directions"]:
        print(f"1. {direction.strip()}", file=file)
    print("\n</div>\n", file=file)


def print_footnotes(data: dict[str, Any], file):
    """Generates unordered list of Ingredients."""
    if not data.get("footnotes"):
        # Not present or empty, skip printing
        return
    print('<div class="recipe-footnotes" markdown>\n', file=file)
    print("### Footnotes", file=file)
    for footnote in data["footnotes"]:
        print(f"- {footnote.strip()}", file=file)
    print("\n</div>\n", file=file)


for file in SRC.rglob("*.md"):
    contents = file.read_text()
    data = frontmatter.loads(contents)

    doc_path = file.relative_to(SRC).with_suffix(".md")
    full_doc_path = Path(OUT, doc_path)

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print(contents, file=fd)

        print('<div class="recipe-contents" markdown>\n', file=fd)

        print_stats(data, file=fd)
        print_ingredients(data, file=fd)
        print_directions(data, file=fd)
        print_footnotes(data, file=fd)

        print("</div>\n", file=fd)
