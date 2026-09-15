"""Checks that an installation is ready to run the course notebooks.

This is the programmatic version of the verification cell in Notebook 00. Run it
after setting the environment up, or when a notebook fails in a way that looks
like it might be the installation rather than the code:

    uv run --group dev pytest

Dataset checks skip rather than fail when a dataset has not been downloaded yet,
since no one needs all of them at once. The preparation notebooks are in Part F.
"""

import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# The packages Notebook 00 tells participants to expect, by import name.
REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "statsmodels",
    "sklearn",
    "pyarrow",
    "IPython",
    "missingno",
    "huggingface_hub",
]

MINIMUM_PYTHON = (3, 13)

# Every dataset the notebooks use: the nb_config constant, the notebook that
# prepares it, and the arguments needed to read it.
DATASETS = [
    ("CDC_TEMP_PATH", "F01b", {}),
    ("OPS_15M_PATH", "F01a", {}),
    ("OPS_30M_PATH", "F01a", {}),
    ("HOUSEHOLD_POWER_PATH", "F01c", {"sep": ";", "decimal": "."}),
    ("AIR_QUALITY_PATH", "F01c", {"sep": ";", "decimal": ","}),
    ("ROSSMANN_TRAIN_PATH", "F01c", {}),
    ("ROSSMANN_STORE_PATH", "F01c", {}),
]


@pytest.mark.env
def test_python_version_matches_requires_python():
    assert sys.version_info >= MINIMUM_PYTHON, (
        f"The course requires Python {'.'.join(map(str, MINIMUM_PYTHON))} or newer, "
        f"but the tests are running on {sys.version.split()[0]}. "
        "Run 'uv sync' and select the project environment as your kernel."
    )


@pytest.mark.env
@pytest.mark.parametrize("package", REQUIRED_PACKAGES)
def test_required_package_is_importable(package):
    importlib.import_module(package)


@pytest.mark.env
def test_notebook_helpers_are_importable():
    """The `src` package holds helpers that the notebooks import directly."""
    importlib.import_module("src.plotting")
    importlib.import_module("src.utils")


@pytest.mark.env
@pytest.mark.parametrize("constant", [name for name, _, _ in DATASETS])
def test_dataset_path_is_declared(constant):
    """Every dataset should have a usable path constant in nb_config."""
    nb_config = importlib.import_module("nb_config")

    assert hasattr(nb_config, constant), f"nb_config is missing {constant}"

    path = getattr(nb_config, constant)
    assert isinstance(path, Path), f"{constant} should be a Path, got {type(path).__name__}"
    assert path.is_absolute(), f"{constant} should be absolute so it works from any directory"
    assert REPO_ROOT in path.parents, f"{constant} should point inside the repository"


@pytest.mark.env
@pytest.mark.parametrize("constant, preparation_notebook, read_options", DATASETS)
def test_dataset_is_readable(constant, preparation_notebook, read_options):
    """A downloaded dataset should be non-empty and readable by pandas."""
    import pandas as pd

    nb_config = importlib.import_module("nb_config")
    path = getattr(nb_config, constant)

    if not path.exists():
        pytest.skip(f"not downloaded yet; run notebook {preparation_notebook}")

    assert path.stat().st_size > 0, f"{path} exists but is empty"

    if path.suffix == ".parquet":
        frame = pd.read_parquet(path)
    else:
        frame = pd.read_csv(path, nrows=5, low_memory=False, **read_options)

    assert not frame.empty, f"{path} parsed to an empty frame"
