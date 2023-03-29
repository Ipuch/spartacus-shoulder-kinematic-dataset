from enum import Enum
from pathlib import Path


class DatasetCSV(Enum):
    """Enum for the dataset csv files, with dynamic path"""

    RAW = Path(__file__).parent.parent / "data" / "only_dataset_raw.csv"
    CLEAN = Path(__file__).parent.parent / "data" / "dataset_clean.csv"
