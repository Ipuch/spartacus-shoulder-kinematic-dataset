import pandas as pd
import numpy as np

from .enums import DatasetCSV
from .row_data import RowData


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

        self.clean_df()
        # self.remove_rows_not_ready_for_analysis() # Todo: remove this function ultimately
        self.rows = []
        self.rows_output = None

        self.confident_dataframe = None
        self.confident_data_values = None

    def clean_df(self):
        # turn nan into None for the following columns
        # dof_1st_euler, dof_2nd_euler, dof_3rd_euler, dof_translation_x, dof_translation_y, dof_translation_z
        self.dataframe = self.dataframe.where(pd.notna(self.dataframe), None)

    def remove_rows_not_ready_for_analysis(self):
        # Todo: remove this function ultimately
        # remove lines I know they are not ready for analysis
        # drop line with "Charbonnier et al." in dataset_authors
        dataset_authors = [
            "Charbonnier et al.",  # no data yet.
            "Gutierrez Delgado et al.",  # not usable finally ?
            "Kim et al.",  # no data yet.
        ]
        for a in dataset_authors:
            self.dataframe.drop(
                self.dataframe[self.dataframe["dataset_authors"].str.contains(a)].index,
                inplace=True,
            )
        article_author_year = [
            "Sahara et al. 2006",  # no rotation data
            "Sugi et al. 2021",
        ]
        for a in article_author_year:
            self.dataframe.drop(
                self.dataframe[self.dataframe["article_author_year"].str.contains(a)].index,
                inplace=True,
            )

    def set_correction_callbacks_from_segment_joint_validity(self, print_warnings: bool = False) -> pd.DataFrame:
        """
        This function will add a callback function to the dataframe.
        Before setting the callback function, it will check the validity of the joint and the segments
        declared in the dataframe.

        !!! It skips the rows that are not valid.

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

    def import_confident_data(self) -> pd.DataFrame:
        """
        This function will import the data from the dataframe, using the callback functions.
        Only the data corresponding to the rows that are considered good and have a callback function will be imported.
        """
        if self.confident_dataframe is None:
            raise ValueError(
                "The dataframe has not been checked yet. " "Use set_correction_callbacks_from_segment_joint_validity"
            )

        output_dataframe = pd.DataFrame(
            columns=[
                "article",
                "joint",
                "angle_translation",
                "degree_of_freedom",
                "legend",
                "humeral_motion",
                "humerothoracic_angle",
                "value",
                "confidence",
            ]
        )

        for i, row in self.confident_dataframe.iterrows():
            row_data = RowData(row)

            row_data.check_all_segments_validity(print_warnings=False)
            row_data.check_joint_validity(print_warnings=False)
            row_data.set_segments()
            row_data.check_segments_correction_validity(print_warnings=False)
            row_data.set_rotation_correction_callback()

            row_data.import_data()
            df_angle_series = row_data.to_angle_series_dataframe()

            # add the row to the dataframe
            output_dataframe = pd.concat([output_dataframe, df_angle_series], ignore_index=True)

        self.confident_data_values = output_dataframe
        return output_dataframe


def load() -> Spartacus:
    """Load the confident dataset"""
    # open the file only_dataset_raw.csv
    df = pd.read_csv(DatasetCSV.CLEAN.value)
    # temporary for debugging
    # df = df[df["dataset_authors"] == "Fung et al."]
    # keep Fung and Bourne
    # df = df[df["dataset_authors"].isin(["Fung et al.", "Bourne"])]
    # df = df[df["dataset_authors"].isin(["Bourne"])]
    # df = df[df["dataset_authors"] == "Chu et al."]
    # df = df[df["dataset_authors"] == "Dal Maso et al."]
    # df = df[df["dataset_authors"] == "Kolz et al."]
    # df = df[df["dataset_authors"] == "Kozono et al."]
    # df = df[df["dataset_authors"] == "Matsumura et al."]
    # df = df[df["dataset_authors"] == "Oki et al."]
    # df = df[df["dataset_authors"] == "Teece et al."]
    # df = df[df["dataset_authors"] == "Yoshida et al."]

    print(df.shape)
    sp = Spartacus(dataframe=df)
    sp.remove_rows_not_ready_for_analysis()
    sp.set_correction_callbacks_from_segment_joint_validity(print_warnings=True)
    sp.import_confident_data()
    # df = load_confident_data(df, print_warnings=True)
    print(df.shape)
    return sp
