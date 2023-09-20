import pandas as pd
import numpy as np

from . import (
    DatasetCSV,
    RowData,
)


class Spartacus:
    """
    This is a Dataset Class.
    The class can have methods to load the data, filter it, or perform common operations in a natural language style.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
    ):
        self.dataframe = dataframe
        self.confident_dataframe = None

    def load(self, print_warnings: bool = False):
        """
        Load the confident dataset

        Parameters
        ---------
        print_warnings: bool
            This displays warning when necessary.
        """
        # columns
        columns = self.dataframe.columns
        # add a callback_function column
        columns = np.append(columns, "callback_function")

        # create an empty dataframe
        self.confident_dataframe = pd.DataFrame(columns=columns)

        # keep article_year == 2008
        # df = df[df["article_year"] == 2008]

        for i, row in self.dataframe.iterrows():
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

            if rotation_validity:
                row_data.set_rotation_correction_callback()

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
            self.confident_dataframe = pd.concat([self.confident_dataframe, row.to_frame().T], ignore_index=True)

        return self.confident_dataframe

    def to_angle_series_dataframe(self):
        """
        Convert the dataframe to angle series dataframe with the following columns:
        "article", "joint", "angle_translation", "degree_of_freedom", "movement", "humerothoracic_angle", "value",
        "humerothoracic_angle".
        """
        # create an empty dataframe
        angle_series_dataframe = pd.DataFrame(
            columns=["article", "joint", "angle_translation", "degree_of_freedom", "movement", "humerothoracic_angle", "value"]
        )

        for i, row in self.confident_dataframe.iterrows():
            # print(row.article_author_year)

            new_row =

            row_data = RowData(row)
            row_data.set_segments()
            row_data.set_rotation_correction_callback()

            # add the callback function to the dataframe
            row.callback_function = row_data.rotation_correction_callback

            # add the row to the dataframe
            angle_series_dataframe = pd.concat([angle_series_dataframe, row.to_frame().T], ignore_index=True)

        return angle_series_dataframe


def load() -> Spartacus:
    """Load the confident dataset"""
    # open the file only_dataset_raw.csv
    df = pd.read_csv(DatasetCSV.CLEAN.value)
    print(df.shape)
    sp = Spartacus(dataframe=df)
    sp.load(print_warnings=False)
    # df = load_confident_data(df, print_warnings=True)
    print(df.shape)
    return sp
