"""Sphinx configuration for the course documentation.

The pages here deliberately hold very little prose of their own. README.md,
FAQ.md, contributing.md and data/datasets.md are the documentation this
repository already had, they are what a reader meets first on GitHub, and
restating them here would create a second copy to keep in step. The pages
include them instead, so each stays a single source of truth.

That leaves one problem to solve: those files link to things by repository
path — notebooks, the licence, reference_scores.py — and a built HTML page
cannot follow a link to a file that is not part of the site. `generate_pages`
below copies each source file into `_generated/` at the start of the build,
rewriting those links to point at GitHub on the way through. The rewriting has
to happen before the file is parsed: MyST resolves markdown links while
parsing, and a link it cannot resolve becomes a broken anchor rather than
something a later transform can repair.

Build with:

    uv run --group docs sphinx-build -b html docs docs/_build/html
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "notebooks"))

# ── Project ──────────────────────────────────────────────────────────────────

project = "Time Series Analysis and Forecasting"
author = "Mario Tormo Romero"
copyright = "KI-Servicezentrum Berlin-Brandenburg, Hasso Plattner Institute"

# Read the version the rest of the repository publishes, rather than repeating it
_pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
release = next(
    line.split('"')[1] for line in _pyproject.splitlines() if line.startswith("version =")
)
version = release

REPO_URL = "https://github.com/aihpi/workshop-time-series"
REPO_BLOB = f"{REPO_URL}/blob/main"

# ── Extensions ───────────────────────────────────────────────────────────────

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

# Notebooks are not rendered here: they are the course, they are large, and
# several take many minutes to execute. The site links to them on GitHub.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}
# Only resolve intersphinx when explicitly asked, so a missing network does not
# turn every unresolved name into a warning
intersphinx_disabled_reftypes = ["*"]

autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": True}

# ── HTML ─────────────────────────────────────────────────────────────────────

html_theme = "furo"
html_title = f"{project} {release}"
html_static_path = ["_static"] if (Path(__file__).parent / "_static").exists() else []
html_theme_options = {
    "source_repository": f"{REPO_URL}/",
    "source_branch": "main",
    "source_directory": "docs/",
}


# ── Repository-relative links in the files we include ───────────────────────

# Prefixes that exist in the repository but not in the built site. A link to any
# of these is sent to GitHub rather than resolved locally.
REPO_PATHS = ("notebooks/", "solutions/", "src/", "tests/", "tools/", "data/",
              "references/", "media/", "artifacts/", "LICENSE", "CODE_OF_CONDUCT.md",
              "README.md", "pyproject.toml")

# Files this site renders itself, so a link to them should stay inside the site
RENDERED_HERE = {
    "FAQ.md": "faq",
    "contributing.md": "contributing",
    "data/datasets.md": "datasets",
}

# Source file -> (generated page name, title to give it)
GENERATED = {
    "FAQ.md": ("faq", "Frequently asked questions"),
    "contributing.md": ("contributing", None),
    "data/datasets.md": ("datasets", None),
}

MARKDOWN_LINK = re.compile(r"\]\(\s*(?!<)([^)\s]+?)\s*\)")


def rewrite_link(target: str) -> str:
    """Point one markdown link at GitHub, or at this site, or leave it alone."""
    if "://" in target or target.startswith(("#", "mailto:")):
        return target

    path, _, anchor = target.partition("#")
    path = path.lstrip("./")
    suffix = f"#{anchor}" if anchor else ""

    if not path:
        return target
    if path in RENDERED_HERE:
        return f"{RENDERED_HERE[path]}.md{suffix}"
    if path.startswith(REPO_PATHS) or path in REPO_PATHS:
        return f"{REPO_BLOB}/{path}{suffix}"
    return target


def generate_pages(app, config):
    """Write the included files into _generated/, with their links rewritten.

    Sphinx parses what is in _generated/, so the files at the repository root
    stay the single copy anyone edits, and stay correct when read on GitHub.
    """
    output = Path(app.srcdir) / "_generated"
    output.mkdir(exist_ok=True)

    for source_name, (page, title) in GENERATED.items():
        text = (REPO_ROOT / source_name).read_text(encoding="utf-8")
        text = MARKDOWN_LINK.sub(lambda m: "](" + rewrite_link(m.group(1)) + ")", text)

        # Images live in the repository, not beside the built page
        text = text.replace('src="./media/', f'src="{REPO_URL}/raw/main/media/')

        if title:
            text = f"# {title}\n\n{text}"

        (output / f"{page}.md").write_text(text, encoding="utf-8")


def setup(app):
    app.connect("config-inited", generate_pages)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
