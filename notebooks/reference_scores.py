"""Results carried from one notebook into another's comparison table.

Several notebooks compare their own model against ones fitted earlier in the
course. Refitting those models would double the runtime of Part D, so the
figures are quoted instead — and a quoted figure goes stale silently the first
time somebody changes a training setting upstream.

This module is the one place they live. It also records two things a bare
number cannot:

**Which series produced it.** Part C and Notebook D01 forecast daily sales for
one Rossmann store, in units of sales; Notebooks D02 to D05 forecast hourly
Austrian electricity load, in megawatts. Those numbers are not comparable, and
`carried()` refuses to build a table that mixes them.

**Which run size produced it.** Notebooks D02, D04 and D05 default to a reduced
workshop configuration and reproduce the quoted figures only with
``FULL_RUN = True``. A comparison that puts a workshop-mode score beside a
full-run reference is not wrong so much as unlabelled, so `carried()` labels it.

Regenerate after changing any training configuration:

    uv run --group dev python tools/refresh_reference_scores.py
"""

from dataclasses import dataclass

# Series identifiers, so incomparable figures cannot be placed side by side
ROSSMANN = "Rossmann store 1, daily sales"
AUSTRIAN_LOAD = "Austrian load, hourly (MW)"


@dataclass(frozen=True)
class Score:
    """One published result, with enough provenance to re-derive it.

    `mae` is always the full-run figure, since that is what the notebooks quote.
    `workshop_mae` is the same model under the notebook's reduced settings, or
    None where the producing notebook has no reduced mode or the value has not
    been measured — `note` says which.
    """

    mae: float
    series: str
    source: str
    seconds: float | None = None
    workshop_mae: float | None = None
    note: str = ""


SCORES = {
    # ── Part B and C, Rossmann store 1 ───────────────────────────────────────
    "SARIMAX (B02)": Score(
        mae=413.8, series=ROSSMANN, source="B02, section 7",
        note="no reduced run mode",
    ),
    "Random forest (C02)": Score(
        mae=232.2, series=ROSSMANN, source="C02, section 4",
        note="no reduced run mode",
    ),
    "LightGBM (C02)": Score(
        mae=240.0, series=ROSSMANN, source="C02, section 5",
        note="no reduced run mode",
    ),
    # ── Part D, Austrian load ────────────────────────────────────────────────
    "LSTM (D02)": Score(
        mae=368.6, series=AUSTRIAN_LOAD, source="D02, section 4", seconds=124,
        workshop_mae=433.5,
    ),
    "LSTM stacked (D02)": Score(
        mae=350.4, series=AUSTRIAN_LOAD, source="D02, section 6", seconds=295,
        workshop_mae=418.8,
    ),
    "Simple CNN (D03)": Score(
        mae=291.6, series=AUSTRIAN_LOAD, source="D03, section 3", seconds=22,
        note="no reduced run mode",
    ),
    "TCN (D03)": Score(
        mae=260.6, series=AUSTRIAN_LOAD, source="D03, section 6", seconds=283,
        note="no reduced run mode",
    ),
    "Transformer (D04)": Score(
        mae=304.2, series=AUSTRIAN_LOAD, source="D04, section 7", seconds=1500,
        workshop_mae=326.7,
    ),
}


def carried(names, series, full_run=True):
    """Rows for a comparison table, drawn from the scores above.

    `series` is the series the calling notebook is itself forecasting; asking
    for a figure from any other one is an error rather than a silent apples-to-
    oranges row. Each row carries the run size its reference came from, so a
    workshop-mode comparison says so on its face.

    `Seconds` is always the full-run timing, including on rows whose MAE came
    from a reduced run: reduced-mode timings have not been measured, and the
    figure is only ever used to show orders of magnitude.
    """
    rows = []

    for name in names:
        if name not in SCORES:
            raise KeyError(f"{name!r} is not in SCORES; known names: {sorted(SCORES)}")

        score = SCORES[name]
        if score.series != series:
            raise ValueError(
                f"{name!r} was measured on {score.series!r}, but this table is "
                f"about {series!r}. These figures are not comparable."
            )

        use_workshop = not full_run and score.workshop_mae is not None
        rows.append({
            "Model": name,
            "Test MAE": score.workshop_mae if use_workshop else score.mae,
            "Reference run": "workshop" if use_workshop else "full",
            "Seconds": score.seconds,
        })

    return rows


def mae(name, series, full_run=True):
    """A single carried figure, with the same checks as `carried`."""
    return carried([name], series, full_run)[0]["Test MAE"]
