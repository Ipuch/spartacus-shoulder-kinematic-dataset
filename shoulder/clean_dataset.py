import pandas as pd

from enums import DatasetCSV


# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.RAW.value)
# clean lines with only NaN
df = df.dropna(how="all")
# rename all the columns with only lower cases
df.columns = [col.lower() for col in df.columns]
# set all the "true" to True and "false" to False
df = df.replace({"true": True, "false": False})
# save the cleaned dataset
df.to_csv(DatasetCSV.CLEAN.value, index=False)

# todo: add a function that fill the cells with that contains the location of dataset with the actual dataset
