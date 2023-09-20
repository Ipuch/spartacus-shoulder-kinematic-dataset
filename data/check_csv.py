"""
This script will load all the csv files in the data folder with pandas and checks the dimension of the pandas dataframe.
It is expected to have only two columns per csv file and at least 1 row.
"""

import os
import pandas as pd

# load all the csv files in the data folder here and its subfolers.
data_folder = os.path.join(os.path.dirname(__file__))

for file in os.listdir(data_folder):
        print("Folder:", file)
        # if not a folder continue
        if not os.path.isdir(os.path.join(data_folder, file)):
            continue

        if file == "Graichen et al 2000":
            continue

        for subfile in os.listdir(os.path.join(data_folder, file)):
            if subfile.endswith(".csv"):
                print("Loading file:", subfile)
                df = pd.read_csv(os.path.join(data_folder, file, subfile), header=None)
                print("Shape:", df.shape)
                print("Columns:", df.columns)
                print(df.head())
                df.columns = ["humerothoracic_angle", "value"]
                print("")

                if df.shape[1] != 2:
                    raise ValueError("The csv file should have only two columns.")
                if df.shape[0] < 1:
                    raise ValueError("The csv file should have at least one row.")


print("All csv files have been loaded successfully.")


