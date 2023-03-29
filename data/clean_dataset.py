import pandas as pd

# open the file only_dataset_raw.csv
df = pd.read_csv("only_dataset_raw.csv")
# clean lines with only NaN
df = df.dropna(how="all")
# rename all the columns with only lower cases
df.columns = [col.lower() for col in df.columns]
# save the cleaned dataset
df.to_csv("dataset_clean.csv", index=False)


