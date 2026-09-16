"""Checks on the documentation sources.

Building the site needs the `docs` group installed, so these do not build it.
They check the things that break without anyone noticing: a page added to the
repository but left out of the navigation, a page referenced by the navigation
but never written, and the helper modules the API page documents still being
importable under the names it uses.

To build the site:

    uv run --group docs sphinx-build -b html docs docs/_build/html
"""

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
INDEX = DOCS_DIR / "index.md"

# Written into docs/_generated/ by conf.py when the site is built
GENERATED_PAGES = {"_generated/datasets", "_generated/faq", "_generated/contributing"}


def toctree_entries():
    """The pages listed in the navigation on the landing page."""
    text = INDEX.read_text(encoding="utf-8")
    block = re.search(r"```\{toctree\}(.*?)```", text, re.S)
    assert block, "index.md has no toctree"

    return [
        line.strip()
        for line in block.group(1).splitlines()
        if line.strip() and not line.strip().startswith(":")
    ]


def test_every_toctree_entry_exists():
    """A page in the navigation is either written, or generated at build time."""
    missing = [
        entry for entry in toctree_entries()
        if entry not in GENERATED_PAGES and not (DOCS_DIR / f"{entry}.md").exists()
    ]
    assert not missing, f"listed in the toctree but not written: {missing}"


def test_every_page_is_in_the_navigation():
    """A page nobody links to is a page nobody reads."""
    written = {
        path.stem for path in DOCS_DIR.glob("*.md")
        if path.name != "index.md"
    }
    listed = set(toctree_entries())
    orphans = sorted(written - listed)
    assert not orphans, f"written but missing from the toctree in index.md: {orphans}"


def test_generated_pages_have_a_source():
    """Each generated page names a file that exists to generate it from."""
    conf = (DOCS_DIR / "conf.py").read_text(encoding="utf-8")
    block = re.search(r"GENERATED = \{(.*?)\n\}", conf, re.S)
    assert block, "conf.py has no GENERATED mapping"

    missing = [
        source for source in re.findall(r'"([^"]+\.md)":', block.group(1))
        if not (REPO_ROOT / source).exists()
    ]
    assert not missing, f"conf.py generates pages from files that do not exist: {missing}"


@pytest.mark.parametrize("module", ["nb_config", "reference_scores"])
def test_documented_notebook_modules_import(module):
    """The API page documents these by name; they have to be importable by it."""
    sys.path.insert(0, str(REPO_ROOT / "notebooks"))
    try:
        __import__(module)
    finally:
        sys.path.pop(0)
