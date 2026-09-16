"""Check the figures in notebooks/reference_scores.py against the notebooks.

The registry stops one notebook's result from being pasted into another by
hand, but it cannot tell whether the figures in it are still true: that only
comes from running the notebooks that produce them. This does that.

It executes each producing notebook with FULL_RUN enabled, reads the scores out
of the executed outputs, and reports any that no longer match. It does not edit
the registry — a changed figure usually means prose needs updating too, and
that is a judgement call.

With ``--prose`` it also checks the other half of the problem the registry
cannot reach: figures written into markdown. For each executed notebook it
lists the numbers its prose quotes that do not appear anywhere in its own
output. That is advisory — prose rounds, restates and does arithmetic on its
figures, so a flagged number is a prompt to look, not a defect. It never fails
the run.

In practice it is quieter than that suggests, and what it finds is worth
finding. Run against D05 it flags the two places the prose quotes 563.3, the
naive baseline from Notebooks D02 and D03, to contrast with the 561.3 this
notebook computes. Both are deliberate, both are cross-notebook references
living in markdown where the registry cannot reach them, and both would go
stale the same silent way a hardcoded score does.

**This takes well over an hour**, because it runs the whole of Part D at full
size. It is a release check, not a test. The fast suite has a separate guard
that catches literals creeping back into the notebooks.

    uv run --group dev python tools/refresh_reference_scores.py
    uv run --group dev python tools/refresh_reference_scores.py --only D03
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

sys.path.insert(0, str(NOTEBOOKS_DIR))
import reference_scores  # noqa: E402  # type: ignore[import-not-found]

# How to recover each figure from its notebook's executed output. The pattern
# runs against every text output of the named notebook, and group 1 is the MAE.
EXTRACTORS = {
    "SARIMAX (B02)": ("B02_ARIMA_models", r"SARIMAX[^\n]*?(\d+\.\d)"),
    "Random forest (C02)": ("C02_Machine_learning_models", r"Random forest\s+(\d+\.\d)"),
    "LightGBM (C02)": ("C02_Machine_learning_models", r"LightGBM\s+MAE\s*=\s*(\d+\.\d)"),
    "LSTM (D02)": ("D02_Recurrent_networks", r"LSTM\s+test MAE\s+(\d+\.\d)"),
    "LSTM stacked (D02)": ("D02_Recurrent_networks", r"LSTM, 2 layers\s+(\d+\.\d)"),
    "Simple CNN (D03)": ("D03_Convolutional_networks", r"Simple CNN: test MAE (\d+\.\d)"),
    "TCN (D03)": ("D03_Convolutional_networks", r"TCN: test MAE (\d+\.\d)"),
    "Transformer (D04)": ("D04_Transformers", r"Transformer: test MAE (\d+\.\d)"),
}


def execute(notebook: str, output_dir: Path) -> Path:
    """Run one notebook at full size and return the executed copy."""
    source = NOTEBOOKS_DIR / f"{notebook}.ipynb"
    patched = output_dir / f"{notebook}.ipynb"

    # FULL_RUN is a plain assignment in the data cell of every notebook that has one
    text = source.read_text(encoding="utf-8")
    patched.write_text(text.replace("FULL_RUN = False", "FULL_RUN = True"), encoding="utf-8")

    print(f"  executing {notebook} ...", flush=True)
    subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute",
         "--inplace", "--ExecutePreprocessor.timeout=10000", str(patched)],
        cwd=NOTEBOOKS_DIR, check=True, capture_output=True,
    )
    return patched


def text_outputs(path: Path) -> str:
    """Every piece of text a notebook printed or displayed."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    chunks = []

    for cell in notebook["cells"]:
        for output in cell.get("outputs", []):
            chunks.append("".join(output.get("text", "")))
            chunks.append("".join(output.get("data", {}).get("text/plain", "")))

    return "\n".join(chunks)


def prose_figures(path: Path):
    """Numbers quoted in a notebook's markdown, paired with their context."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    quoted = []

    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        text = "".join(cell["source"])
        for match in re.finditer(r"\b\d{2,5}\.\d+\b", text):
            start = max(0, match.start() - 45)
            context = text[start:match.end() + 25].replace("\n", " ")
            quoted.append((match.group(0), cell.get("id"), context.strip()))

    return quoted


def report_prose(path: Path, outputs: str) -> int:
    """List prose figures absent from the notebook's own output. Advisory only."""
    unmatched = []

    for number, cell_id, context in prose_figures(path):
        # Accept the figure as printed, and as the output would round it
        value = float(number)
        candidates = {number, f"{value:g}", f"{value:.1f}", f"{value:.0f}", f"{value:.2f}"}
        if not any(candidate in outputs for candidate in candidates):
            unmatched.append(f"    {number:>9}  {cell_id or '?':<22} ...{context}...")

    if unmatched:
        print(f"  {path.stem}: {len(unmatched)} prose figure(s) not found in its own output")
        for line in unmatched[:12]:
            print(line)
        if len(unmatched) > 12:
            print(f"    ... and {len(unmatched) - 12} more")

    return len(unmatched)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", default=None,
                        help="limit to one producing notebook, e.g. D03")
    parser.add_argument("--prose", action="store_true",
                        help="also report markdown figures absent from a notebook's own output")
    arguments = parser.parse_args()

    wanted = {
        name: (notebook, pattern)
        for name, (notebook, pattern) in EXTRACTORS.items()
        if arguments.only is None or any(prefix in notebook for prefix in arguments.only)
    }
    if not wanted:
        print("nothing selected")
        return 1

    stale, missing = [], []

    with tempfile.TemporaryDirectory() as directory:
        output_dir = Path(directory)
        executed: dict[str, str] = {}

        for name, (notebook, pattern) in wanted.items():
            if notebook not in executed:
                executed[notebook] = text_outputs(execute(notebook, output_dir))

            match = re.search(pattern, executed[notebook])
            recorded = reference_scores.SCORES[name].mae

            if match is None:
                missing.append(f"{name}: pattern {pattern!r} found nothing in {notebook}")
                continue

            found = float(match.group(1))
            status = "ok" if abs(found - recorded) < 0.05 else "STALE"
            print(f"  {status:5s} {name:22s} registry {recorded:7.1f}   notebook {found:7.1f}")
            if status == "STALE":
                stale.append(f"{name}: registry says {recorded}, {notebook} produced {found}")

        if arguments.prose:
            print()
            print("Prose figures (advisory; rounding and restatement cause false alarms):")
            total = sum(
                report_prose(output_dir / f"{notebook}.ipynb", outputs)
                for notebook, outputs in executed.items()
            )
            if not total:
                print("  every figure quoted in prose appears in its notebook's output")

    print()
    for problem in missing:
        print(f"could not check: {problem}")
    for problem in stale:
        print(f"STALE: {problem}")

    if stale or missing:
        print("\nUpdate notebooks/reference_scores.py, and check the prose that quotes "
              "these figures — the registry does not cover markdown.")
        return 1

    print("every figure in reference_scores.py matches its notebook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
