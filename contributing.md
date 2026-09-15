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
```

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

## Code of Conduct

Please note that all contributions should adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Ensure respectful and inclusive communication throughout the contribution process.

Thank you for helping make this course better!
