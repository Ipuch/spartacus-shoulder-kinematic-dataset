import pandas as pd
import numpy as np

from shoulder import (
    DatasetCSV,
    RowData,
)


def load_confident_data(df: pd.DataFrame, print_warnings: bool = False) -> pd.DataFrame:
    """Load the confident data from the dataset"""

    # columns
    columns = df.columns
    # add a callback_function column
    columns = np.append(columns, "callback_function")

    # create an empty dataframe
    df_confident = pd.DataFrame(columns=columns)

    # keep article_year == 2008
    # df = df[df["article_year"] == 2008]

    for i, row in df.iterrows():
        # print(row.article_author_year)

        row_data = RowData(row)
        if print_warnings:
            print("")
            print("")
            print("")
            print("row_data.joint", row.article_author_year)

        if not row_data.check_all_segments_validity(print_warnings=print_warnings):
            continue
        if not row_data.check_joint_validity(print_warnings=print_warnings):
            continue
        row_data.set_segments()
        rotation_validity, translation_validity = row_data.check_segments_correction_validity(
            print_warnings=print_warnings
        )
        if not rotation_validity and not translation_validity:
            print("WARNING : No usable data for this row, in both rotation and translation...")
            continue

        # if rotation_validity:
        #     row_data.set_rotation_correction_callback()

        if not row_data.usable_rotation_data:
            if print_warnings:
                print("WARNING : inconsistency in the dataset")
                print(row.joint, row.article_author_year)
                print("detected :", row_data.joint.joint_type)
                print("detected parent segment :", row.parent)
                row_data.parent_biomech_sys.__print__()
                print("detected child segment :", row.child)
                row_data.child_biomech_sys.__print__()
                print("detected joint coordinate system :", row_data.joint.euler_sequence)
                print("callback function :", row_data.rotation_correction_callback)
            continue
        # add the callback function to the dataframe
        row.callback_function = row_data.rotation_correction_callback

        # add the row to the dataframe
        df_confident = pd.concat([df_confident, row.to_frame().T], ignore_index=True)

    return df_confident


# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.CLEAN.value)
print(df.shape)
df = load_confident_data(df, print_warnings=True)
print(df.shape)
