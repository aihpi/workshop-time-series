<div style="background-color: #ffffff; color: #000000; padding: 30px;">
    <p style="text-align:right;"><img src="./media/images/kisz_logo.png" alt="kisz logo" width="192" height="69" style="margin-right: 30px; margin-bottom:30px;"></p>
    <h1 style="text-align:center;"> Frequently Asked Questions </h1>
</div>

This page collects the questions that come up most often in the course forum. If your question is
not answered here, please ask it in the [course forum on
OpenHPI](https://open.hpi.de/courses/timeseries2025) — we add the most useful ones to this page as
the course goes on.

**Contents**

- [Setup and environment](#setup-and-environment)
- [Running the notebooks](#running-the-notebooks)
- [Datasets](#datasets)
- [Course materials and updates](#course-materials-and-updates)
- [Reusing the material](#reusing-the-material)

---

## Setup and environment

### Do I have to use `uv`? Can I use conda or plain pip instead?

You can, but we only support `uv`. The repository ships a `uv.lock` file that pins every dependency
to an exact version, which is what lets us guarantee that the notebooks behave the same way on your
machine as they do on ours. If you install the packages yourself from `pyproject.toml` with conda or
pip, everything will most likely work, but you are on your own if a version difference causes a
problem.

Full setup instructions are in [notebook 00](./notebooks/00_Practical_Introduction.ipynb).

### `uv: command not found` after installing it

The installer puts `uv` in `~/.local/bin` (macOS/Linux) or `%USERPROFILE%\.local\bin` (Windows) and
adds that directory to your `PATH`. The change only applies to *new* terminal sessions, so close
your terminal and open a new one, then try `uv --version` again.

If it still is not found, either add that directory to your `PATH` manually, or install uv into an
existing Python instead:

```bash
pip install uv
```

### `uv sync` fails with a Python version error

The project requires **Python 3.13 or newer** (see `requires-python` in `pyproject.toml`). You do
not need to install it yourself — `uv` will download a suitable interpreter for you. If it refuses
to, run:

```bash
uv python install 3.13
uv sync
```

### The verification cell in notebook 00 shows red crosses

That cell checks the packages the course needs against the interpreter the notebook is currently
running on. A red cross almost always means the notebook is running on the wrong kernel rather than
that a package is missing.

1. In your terminal, from the repository root, run `uv sync`.
2. In the notebook, check the kernel shown in the top-right corner of VS Code. It has to be the
   `.venv` inside the repository folder. If it is not, click it, choose *Python Environments...*,
   and select that one.
3. Restart the kernel with the **Restart** button in the notebook toolbar, and run the cell again.

### VS Code does not offer `.venv` in the kernel picker

Two things are worth checking:

- **The folder you opened.** VS Code has to be opened on the repository root, the folder containing
  `pyproject.toml`. If you opened the `notebooks/` folder, or a parent folder, it will not find the
  environment.
- **The extensions.** You need both **Python** (`ms-python.python`) and **Jupyter**
  (`ms-toolsai.jupyter`). Install them from the Extensions view and reload the window.

If the environment still does not appear, make sure `uv sync` actually created it: there should be a
`.venv` folder in the repository root.

### A notebook says a package is not installed

Almost everything the course needs is installed by `uv sync`. Two things are kept out of it, because they
are large and only some notebooks use them:

```bash
uv sync --group advanced   # Prophet, for one section of Notebook B03
uv sync --group dl         # PyTorch and NeuralForecast, for Part D
```

Notebooks that need an optional package check for it and skip cleanly when it is missing, so you can work
through the rest of them either way.

Part D is the heavy one: PyTorch is around 700 MB on its own. It is installed from PyTorch's CPU-only
index, so you are not also downloading a couple of gigabytes of GPU runtime you will not use.

### Can I use JupyterLab or PyCharm instead of VS Code?

Yes. The course assumes VS Code, but nothing in the material depends on it — any editor that runs
Jupyter notebooks works, as long as the notebook kernel is the project environment (`.venv` in the
repository root).

JupyterLab is not part of the environment we ship, so add it first:

```bash
uv add jupyterlab
uv run jupyter lab
```

Started that way, its default kernel is already the project environment.

---

## Running the notebooks

### `ModuleNotFoundError: No module named 'nb_config'`

`nb_config.py` lives in the `notebooks/` folder, next to the notebooks themselves. This error means
your kernel was started from a different working directory. Start Jupyter from the repository root
and open the notebooks through the file browser, rather than starting it from somewhere else on your
disk.

### `ModuleNotFoundError: No module named 'src'`

Some notebooks use helper functions from the `src/` package. Access to it is set up by `nb_config`,
so `import nb_config` has to come **before** the `from src... import ...` line. If you rearranged
the imports, put `import nb_config` back on top and restart the kernel.

### A cell fails with a `NameError` or a `KeyError` about a column

The notebooks are written to be run from top to bottom: later cells depend on variables and on
DataFrame modifications made by earlier ones. If you jumped into the middle of a notebook, or ran
the same cell twice after it modified a DataFrame in place, use *Run > Restart Kernel and Run All
Cells* to get back to a clean state.

### Do I have to do the exercises?

No, but we strongly recommend it. Exercises are marked with a 🏋️ icon. Attempting one before
reading the solution is what makes the concept stick, even when your attempt does not work.

---

## Datasets

### Where are the datasets? The `data/` folder is almost empty

Datasets are deliberately not stored in this repository — they are too large for git, and some of
them come with licences that do not allow redistribution. You download them once, and they land in
`data/`, which git ignores.

There are two kinds, and an appendix notebook prepares each of them:

- **Prepared datasets**, which we host on Hugging Face —
  [F01a](./notebooks/F01a_Preparing_OPS_datasets.ipynb) and
  [F01b](./notebooks/F01b_Preparing_CDC_dataset.ipynb).
- **External datasets**, which come from their original publisher and land in `data/external/` —
  [F01c](./notebooks/F01c_Preparing_external_datasets.ipynb).

Both kinds, with their links, are listed in [`data/datasets.md`](./data/datasets.md).

### Why do I have to download the Rossmann data by hand?

It is Kaggle competition data. Kaggle requires every user to accept the competition rules with their
own account before downloading, which is not something we can do for you, and the rules do not let us
redistribute the files ourselves. Section 5 of
[F01c](./notebooks/F01c_Preparing_external_datasets.ipynb) walks you through it — it takes a minute,
and the notebook then checks that the files landed in the right place.

The two UCI datasets have no such restriction, so F01c downloads those for you automatically.

### `FileNotFoundError` when a notebook loads its data

The dataset that notebook needs has not been downloaded yet. Check the data-loading cell at the top
of the notebook to see which path it expects, then get that dataset as described above. All paths
are defined as constants in `notebooks/nb_config.py`, so you can look up exactly where a file is
expected to be.

### Why do you not just use one dataset for the whole course?

Different techniques need different data. Detecting outliers is best learned on a dataset that
actually contains outliers, seasonality is best shown on data with a strong yearly cycle, and so on.
Working with several sources is also closer to what real projects look like.

### Can I use my own data?

Absolutely, and it is a very good way to learn. Be aware that the notebooks make assumptions about
column names and about the sampling frequency of the data, so you will have to adapt the code. If
you run into something surprising in your own data, the course forum is a good place to bring it up.

---

## Course materials and updates

### Where are the slides?

In [`references/slides/`](./references/slides/). Extra reading material for each week is in
[`references/resources/`](./references/resources/).

### A notebook listed in the README does not exist yet

The course materials are released gradually, week by week, so the README describes the full course
while the repository only contains what has been published so far. Links to notebooks that have not
been released yet will not work until they are.

### How do I get the new materials?

Pull the latest changes:

```bash
git fetch origin
git merge origin/main
```

We recommend working on your own branch (`git checkout -b my-work`) from the start, so that your own
notes and experiments do not collide with the incoming updates.

### `git merge` reports a conflict in a notebook I edited

Notebooks are JSON files, and git cannot merge them sensibly. The simplest way out is to keep the
incoming version and move your own work aside:

```bash
git checkout --theirs notebooks/<the_notebook>.ipynb
git add notebooks/<the_notebook>.ipynb
```

To avoid this in the first place, do your own experiments in a copy of the notebook (for example
`A01_Loading_data_my_notes.ipynb`) rather than in the original file.

---

## Reusing the material

### Can I use these materials in my own teaching or at work?

Yes. The code is licensed under the [GNU GPL v3](./LICENSE), which allows you to use, modify, and
redistribute it as long as you keep the same licence and attribute the original. Note that the
**datasets** are not ours — each one has its own licence and terms of use, listed at the source
linked in [`data/datasets.md`](./data/datasets.md).

### I found a mistake / I have a suggestion

Please open an issue in the repository — there are templates for bug reports, feature requests, and
content changes. Pull requests are welcome too; see [`contributing.md`](./contributing.md) and our
[code of conduct](./CODE_OF_CONDUCT.md).
