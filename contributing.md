# Contributing Guidelines

Thank you for considering contributing! We appreciate your efforts to make this course better. To ensure a smooth collaboration, please follow these guidelines when contributing.

## Ways to Contribute

### 1. Questions

If you have questions related to the course, code, or any other aspect, you can check the Discussions:

1. Check existing issues and discussions to see if your question has been addressed.
2. If not, open a new discussion.
3. Clearly state your question, providing as much detail as possible.
4. Be patient and respectful while waiting for a response from the community or our team.

### 2. Suggesting Corrections or Improvements to the Code

If you find bugs or have suggestions for improving the code, please follow these steps:

1. Create a new issue in the repository.
2. Use the "Bug Report" template if reporting a bug, or the "Feature Request" template for suggesting improvements.
3. Provide a clear and concise description of the issue or suggestion.
4. You can include relevant details, such as the environment, steps to reproduce the issue, and expected behavior.

### 3. Suggesting Changes to the Content

If you have ideas for modifying or enhancing the course content, follow these steps:

1. Open a new issue using the "Content Change" template.
2. Clearly state the proposed changes or additions.
3. Provide context on why you think the changes are necessary or beneficial.
4. You can include any relevant links or references to support your suggestions.

### 4. Reporting Errors

To report any errors in the documentation, instructions, or any other aspect of the project, use the following steps:

1. Create a new issue with the "Documentation Issue" template.
2. Clearly describe the error and its location.
3. If possible, suggest corrections or improvements.
4. Include any relevant screenshots or examples.

### 5. Any Other Contributions

If you have other ideas, features, or contributions in mind that are not covered above, follow these general steps:

1. Open a new issue with an appropriate template or a custom description.
2. Clearly explain your proposed contribution and its purpose.
3. Provide any necessary details to help understand and implement your contribution.

## Working on the Code

The course environment installs only what the notebooks need, so that participants get a small,
predictable install. Anything else lives in an optional group, and `uv sync` installs none of them:

```bash
uv sync --group dev        # pytest, nbconvert, nbclient: authoring and checking
uv sync --group advanced   # prophet, used by one section of Notebook B03
uv sync --group dl         # torch and neuralforecast, used by Part D
```

`torch` resolves from PyTorch's CPU-only index on Linux and Windows, configured in `pyproject.toml`.
The default PyPI wheels on those platforms carry a CUDA runtime of over 2 GB that this course never uses.

Notebooks that rely on an optional package must check for it and skip cleanly when it is missing, the
way B03 does, so that a default install can still run them end to end.

Check the environment itself with the test suite. It verifies the Python version, the packages the
notebooks need, and that every dataset path constant resolves; datasets you have not downloaded are
skipped rather than failed:

```bash
uv run --group dev pytest
```

With `nbconvert` you can also execute a notebook from the terminal to check that it still runs from
top to bottom, without touching the file in the repository:

```bash
uv run --group dev jupyter nbconvert --to notebook --execute \
    --output-dir /tmp --output check.ipynb notebooks/A05_Forecasting_baselines.ipynb
```

Please run that check on any notebook you change, and clear the outputs before committing: stored
plots make notebooks large and their diffs unreadable.

### Figures carried between notebooks

Several notebooks compare their own model against ones fitted earlier in the course, rather than
refitting them and doubling the runtime of Part D. Those figures live in
[`notebooks/reference_scores.py`](notebooks/reference_scores.py), not as literals in the notebook that
quotes them, so that a training change upstream does not leave stale numbers scattered downstream. The
test suite fails if a published figure is written out by hand.

If you change a training setting, the registry will not notice on its own. Check it with:

```bash
uv run --group dev python tools/refresh_reference_scores.py --only D03
```

That re-executes the producing notebooks at full size and reports any figure that no longer matches, so
it takes well over an hour for the whole set. It deliberately does not edit anything: a changed score
usually means the surrounding prose needs rewriting too, and the registry cannot do that for you.

### Documentation

The site under `docs/` is built with Sphinx:

```bash
uv run --group docs sphinx-build -b html docs docs/_build/html
```

It holds very little prose of its own. `FAQ.md`, this file and `data/datasets.md` are pulled in at build
time, with their repository-relative links rewritten to point at GitHub, so each stays a single copy that
is correct both here and on the site. The pages that are genuinely new are the setup guide, the
maintainer notes, and the reference for the helper modules.

## Code of Conduct

Please note that all contributions should adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Ensure respectful and inclusive communication throughout the contribution process.

Thank you for helping make this course better!
