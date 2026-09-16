"""Where every dataset lives.

Paths are derived from this file's own location, so a notebook finds its data
wherever the repository is cloned and whichever directory Jupyter was started
in. Notebooks import from here rather than writing paths of their own, which is
why moving a dataset is a one-line change.

The datasets themselves are not in the repository. The appendix notebooks in
Part F download them into the directories named below; `data/datasets.md`
documents where each one comes from and under what licence.
"""

import sys
from pathlib import Path

sys.path.append("..")


BASE_DIR = Path(__file__).parent
ARTIFACTS_PATH = BASE_DIR.parent / "artifacts"
DATA_PATH = BASE_DIR.parent / "data"
RAW_DATA_PATH = DATA_PATH / "raw"
EXTERNAL_DATA_PATH = DATA_PATH / "external"
INTERIM_DATA_PATH = DATA_PATH / "interim"
PROCESSED_DATA_PATH = DATA_PATH / "processed"

# ── Dataset paths ─────────────────────────────────────────────────────────────

# CDC: regional monthly air temperature for Germany
CDC_TEMP_PATH = RAW_DATA_PATH / "cdcdata" / "cdc_monthly_regional_air_temp_D.parquet"

# OPS: electricity consumption data (15-min and 30-min variants)
OPS_15M_PATH = RAW_DATA_PATH / "opsdata" / "ops_data_15min.parquet"
OPS_30M_PATH = RAW_DATA_PATH / "opsdata" / "ops_data_30min.parquet"

# ── External datasets ─────────────────────────────────────────────────────────
# Not hosted on Hugging Face. Notebook F01c downloads them, or explains how to
# obtain them where the licence does not allow us to redistribute them.

# UCI: individual household electric power consumption (1-min resolution)
HOUSEHOLD_POWER_DIR = EXTERNAL_DATA_PATH / "Household_Power_Consumption_Dataset"
HOUSEHOLD_POWER_PATH = HOUSEHOLD_POWER_DIR / "household_power_consumption.txt"

# UCI: air quality measurements from a multisensor device (hourly)
AIR_QUALITY_DIR = EXTERNAL_DATA_PATH / "Air_Quality_Dataset"
AIR_QUALITY_PATH = AIR_QUALITY_DIR / "AirQualityUCI.csv"

# Kaggle: Rossmann store sales (daily)
ROSSMANN_DIR = EXTERNAL_DATA_PATH / "Rossmann_Store_Sales_Dataset"
ROSSMANN_TRAIN_PATH = ROSSMANN_DIR / "train.csv"
ROSSMANN_STORE_PATH = ROSSMANN_DIR / "store.csv"
