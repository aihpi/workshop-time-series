# Maintaining the notebooks

Notes for anyone changing the course material. [Contributing](_generated/contributing.md) covers how to propose a
change; this page covers what to know before making one.

## The tests do not run the notebooks

`uv run --group dev pytest` finishes in about three seconds, because nothing it does executes a notebook.
It checks two kinds of thing:

**The environment** — the Python version, that every package the notebooks import is importable, that the
helper modules resolve, and that each dataset path exists. Datasets you have not downloaded are skipped
rather than failed, naming the appendix notebook that fetches them.

**The structure of each notebook** — every cell has an id; no cell's last expression is stranded inside an
`if` or a `for`, where Jupyter would silently display nothing; no relative link points at a file that does
not exist; every contents entry points at a heading that exists; no markdown cell contains a literal tab,
which is what a mangled LaTeX escape leaves behind.

Those are the mistakes that are easy to make and hard to notice. Whether a notebook still *runs* is a
separate question, and the answer costs minutes to hours:

```bash
uv run --group dev jupyter nbconvert --to notebook --execute \
    --output-dir /tmp --output check.ipynb notebooks/A05_Forecasting_baselines.ipynb
```

Run that on any notebook you change, and clear the outputs before committing.

## Run modes

Notebooks D02, D04 and D05 have a `FULL_RUN` switch near the top. The default is `False`, which trains on
a subset and finishes in the few minutes a workshop session has; `True` reproduces the figures quoted in
the prose and takes considerably longer — D04 at full size is around 25 minutes.

Two consequences worth holding on to:

- **A number in the prose of those notebooks is a full-run number.** If you are checking a claim, set
  `FULL_RUN = True` first or you will be comparing against a different model.
- **The reduced mode is not merely a faster version of the same thing.** Notebook D02's own exercise
  measures the difference: its LSTM scores 368.6 MW at full size and 433.5 in workshop mode. One of the
  notebook's conclusions changes between the two, which the text says so at the point it matters.

Notebooks D01 and D03 have no reduced mode; they always train on everything.

## Figures carried between notebooks

Several notebooks compare their own model against ones fitted earlier in the course rather than refitting
them, which would double the runtime of Part D. Those figures live in
[`notebooks/reference_scores.py`](https://github.com/aihpi/kisz-time-series/blob/main/notebooks/reference_scores.py),
not as literals in the notebook that quotes them.

The registry records more than the number, because a bare number cannot be checked:

**Which series produced it.** Part C and Notebook D01 forecast daily sales for one Rossmann store; D02 to
D05 forecast hourly Austrian load in megawatts. Those figures are not comparable, and asking for one in a
table about the other raises rather than producing a misleading row.

**Which run size produced it.** Every quoted figure is a full-run number, but the notebooks that quote
them often default to workshop mode. Rows carry the run they came from, and D04's comparison table shows
it, so a reader in workshop mode can see which references are workshop-mode and which are not.

A test fails if one of the registry's published figures is written into a notebook by hand again. It
checks the registry's own values, which is the regression that actually happens; it does not try to detect
a *new* carried figure, because doing that generically flags too much honest arithmetic to be useful.

### When you change a training setting

The registry does not notice on its own. Check it:

```bash
uv run --group dev python tools/refresh_reference_scores.py --only D03
```

That re-executes the producing notebooks at full size and reports any figure that no longer matches. For
the whole set it takes well over an hour, so it is a release check rather than something to run on every
commit. It deliberately does not edit anything: a changed score usually means the surrounding prose needs
rewriting too, and no tool can do that for you.

Adding `--prose` also lists figures quoted in markdown that do not appear in that notebook's own output.
That part is advisory — prose rounds, restates and does arithmetic on its numbers — but it finds real
things. Run against D05 it flags the two places the prose quotes 563.3, a baseline from Notebooks D02 and
D03, which are cross-notebook references living in markdown where the registry cannot reach them.

## Exercises and solutions

Every notebook with exercises has a matching notebook in
[`solutions/`](https://github.com/aihpi/kisz-time-series/blob/main/solutions/), linked from its footer.
The solutions are checked by the same structural tests as the notebooks.

If you add or change an exercise, **run it before you write the prompt**. Several prompts in this course
originally asserted an outcome the data did not support — a leakage exercise that promised an
extraordinary score from a leak worth 3 MAE, a pruning exercise that asked how many rows dropping a
feature buys back when that feature survives the cut. Each was found by writing the solution and each made
a better exercise once corrected. A prompt that tells the student what they will find is a prompt that has
to be right.

## Building this site

```bash
uv run --group docs sphinx-build -b html docs docs/_build/html
```

The pages here hold almost no prose of their own. `README.md`, `FAQ.md`, `contributing.md` and
`data/datasets.md` are included rather than restated, so there is one copy of each to keep correct. Those
files are written to be read on GitHub and link to notebooks by repository path; `docs/conf.py` rewrites
such links to point at GitHub, so they work in both places without the source files knowing about Sphinx.
