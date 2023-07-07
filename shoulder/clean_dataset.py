import pandas as pd

from enums import DatasetCSV


# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.RAW.value, delimiter=",")
print(df.iloc[0, 0])
assert df.iloc[0, 0] == "Bourne"
assert len(df.iloc[0, :]) == 66
# rename all the columns with only lower cases
df.columns = [col.lower() for col in df.columns]
# clean lines with only NaN
df = df.dropna(how="all")

# set all the "true" to True and "false" to False
df = df.replace({"true": True, "false": False})
# remove extra spaces in the columns with false and true
df = df.replace({"true ": True, "false ": False})
# make column type to bool
df["thorax_is_isb"].astype(bool)
df["humerus_is_isb"].astype(bool)
df["scapula_is_isb"].astype(bool)
df["clavicle_is_isb"].astype(bool)
# all "nan" to np.nan
df = df.replace({"nan": None})

# save the cleaned dataset
df.to_csv(DatasetCSV.CLEAN.value, index=False)

# todo: add a function that fill the cells with that contains the location of dataset with the actual dataset
