# Setting up

The full walkthrough, with screenshots and the VS Code specifics, is in
[`notebooks/00_Practical_Introduction.ipynb`](https://github.com/aihpi/workshop-time-series/blob/main/notebooks/00_Practical_Introduction.ipynb).
This page is the short version, for checking an installation or getting moving quickly.

## What you need

- **Python 3.13 or newer.**
- **[uv](https://docs.astral.sh/uv/)**, which manages the environment and the dependencies.
- **VS Code** with the Python and Jupyter extensions, which is what the course assumes.

## Install

```bash
git clone https://github.com/aihpi/workshop-time-series.git
cd workshop-time-series
uv sync
```

`uv sync` on its own installs exactly what the notebooks need and nothing more. The heavier pieces are
opt-in, because most of the course does not need them:

```bash
uv sync --group dl        # PyTorch and NeuralForecast, for Part D
uv sync --group advanced  # Prophet, for Notebook B03
```

:::{warning}
`uv sync --group dl` replaces the installed set rather than adding to it, so it removes anything from
another group. Name every group you want in one command:

```bash
uv sync --group dl --group advanced --group dev
```
:::

## Check it worked

```bash
uv run --group dev pytest
```

This is the fastest way to find out whether the environment is complete. It checks the Python version,
that every package the notebooks import is importable, that the helper modules resolve, and that each
dataset path is where the notebooks expect it. Datasets you have not downloaded yet are reported as
skipped, naming the appendix notebook that fetches them — so a fresh clone is expected to show seven
skips, not failures.

## Then

Open `notebooks/00_Practical_Introduction.ipynb`, select the `kisz-time-series` kernel, and work forward
from Part A. The appendix notebooks in Part F download the datasets; run the relevant one before starting
each part, or see [Datasets](_generated/datasets.md).
