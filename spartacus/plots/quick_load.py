import os
import pandas as pd
from pathlib import Path

from spartacus.src.enums import DatasetCSV
from ..src.load import load


def import_data():
    """Import the data from the confident_data.csv file if it exists, otherwise it's computed from the raw data."""
    if "confident_data.csv" in os.listdir(str(Path(DatasetCSV.CLEAN.value).parent)):
        return pd.read_csv(Path(DatasetCSV.CLEAN.value).parent / "confident_data.csv")
    else:
        return load().import_confident_data()
