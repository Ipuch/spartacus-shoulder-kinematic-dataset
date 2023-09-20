import numpy as np
import pandas as pd

from .enums import DatasetCSV

# open clean dataset
df = pd.read_csv(DatasetCSV.CLEAN.value)
# do descriptive statistics on each column by printing number of occurences of each value in column
columns = [
    "article_year",
    "experimental_mean",
    "in_vivo",
    "type_of_movement",
    "humeral_motion",
    "joint",
    "active",
    "posture",
    "source_extraction",
]
for col in columns:
    print(col)
    print(df[col].value_counts())


# pivot table by "type_of_movement", "humeral_motion", "joint"
# and display the table
pivoted_df = df.pivot_table(
    index=["humeral_motion", "joint"], values=["number_of_shoulders"], aggfunc={"number_of_shoulders": np.sum}
)
print(pivoted_df)
print("yeah")
