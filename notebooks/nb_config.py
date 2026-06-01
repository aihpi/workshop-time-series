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
