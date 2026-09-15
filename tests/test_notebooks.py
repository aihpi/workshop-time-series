"""Structural checks on the course notebooks.

These do not execute anything, so they are fast enough to run on every change.
They catch the mistakes that are easy to make and hard to notice when a notebook
is authored or edited:

- a result that never displays, because its expression is indented inside a block;
- a link to a notebook or file that does not exist;
- a contents entry pointing at a heading id that was never added.

To check that a notebook still *runs*, execute it; see contributing.md.
"""

import ast
import json
import re
from pathlib import Path

import pytest

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))

# Calls whose return value is not meant to be displayed
STATEMENT_CALLS = {"print", "show", "close", "append", "add", "update", "extend", "sort"}


def notebook_ids():
    return [path.name for path in NOTEBOOKS]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def code_cells(notebook):
    return [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]


def called_name(node):
    """Dotted name of a call, e.g. 'plt.show' -> 'plt.show'."""
    func, parts = node.func, []
    while isinstance(func, ast.Attribute):
        parts.append(func.attr)
        func = func.value
    if isinstance(func, ast.Name):
        parts.append(func.id)
    return ".".join(reversed(parts))


def test_notebooks_exist():
    assert NOTEBOOKS, f"no notebooks found in {NOTEBOOKS_DIR}"


@pytest.mark.parametrize("name", notebook_ids())
def test_every_cell_has_an_id(name):
    """nbformat 4.5 requires cell ids, and they keep diffs readable."""
    notebook = load(NOTEBOOKS_DIR / name)
    missing = [i for i, cell in enumerate(notebook["cells"]) if not cell.get("id")]
    assert not missing, f"cells without an id at positions {missing}"


@pytest.mark.parametrize("name", notebook_ids())
def test_no_result_is_trapped_inside_a_block(name):
    """A cell's last expression only displays if it is at the top level.

    Writing

        if AVAILABLE:
            results.round(1)

    silently produces no output, which is easy to miss when the cell above it
    printed something.
    """
    notebook = load(NOTEBOOKS_DIR / name)
    trapped = []

    for cell in code_cells(notebook):
        try:
            tree = ast.parse("".join(cell["source"]))
        except SyntaxError:
            continue
        if not tree.body:
            continue

        last = tree.body[-1]
        if not isinstance(last, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            continue

        body = getattr(last, "body", [])
        if not body or not isinstance(body[-1], ast.Expr):
            continue

        value = body[-1].value
        if isinstance(value, ast.Call) and called_name(value).split(".")[-1] in STATEMENT_CALLS:
            continue

        trapped.append(f"{cell.get('id')}: {ast.unparse(value)[:60]}")

    assert not trapped, "expression will not display; move it to the top level:\n  " + "\n  ".join(trapped)


@pytest.mark.parametrize("name", notebook_ids())
def test_relative_links_resolve(name):
    """Links to other notebooks and repository files should not 404."""
    notebook = load(NOTEBOOKS_DIR / name)
    broken = []

    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        for target in re.findall(r"\]\(([^)]+)\)", "".join(cell["source"])):
            if target.startswith(("http://", "https://", "#")):
                continue
            path = (NOTEBOOKS_DIR / target.split("#")[0]).resolve()
            if not path.exists():
                broken.append(target)

    # Notebooks released later in the course are linked before they exist
    unwritten = [target for target in broken if re.search(r"/[A-F]\d\d[_a-zA-Z]*\.ipynb$", target)]
    real = [target for target in broken if target not in unwritten]

    assert not real, f"broken links: {real}"


@pytest.mark.parametrize("name", notebook_ids())
def test_contents_anchors_have_matching_headings(name):
    """Every '[Section](#anchor)' needs a heading carrying that id."""
    notebook = load(NOTEBOOKS_DIR / name)
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])

    anchors = set(re.findall(r"\]\(#([^)]+)\)", source))
    headings = set(re.findall(r"<h[1-6][^>]*\sid=\"([^\"]+)\"", source))

    assert not anchors - headings, f"contents links with no matching heading id: {sorted(anchors - headings)}"
