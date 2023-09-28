"""
This script converts all Excel files in a folder to CSV files.
Please install xlrd before running this script.

conda install -c conda-forge xlrd
"""

import pandas as pd
import os


def xls_to_csv(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Write the data to a CSV file
    df.to_csv(output_file, index=False)


def convert_folder(input_folder):
    # Loop through all files in the specified folder
    for filename in os.listdir(input_folder):
        # Check if the file is an Excel file with .xls extension
        if filename.endswith('.xls'):
            # Construct full file paths
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(input_folder, filename.split('.')[0] + '.csv')

            # Convert the Excel file to CSV
            xls_to_csv(input_path, output_path)
            print(f"Converted {input_path} to {output_path}")


convert_folder('/home/puchaud/Projets_Python/shoulder-kinematic-dataset/spartacus/data/Kolz et al 2020')