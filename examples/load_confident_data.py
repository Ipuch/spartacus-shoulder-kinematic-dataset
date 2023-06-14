import pandas as pd
import numpy as np

from shoulder import (
    DatasetCSV,
    Joint,
    check_parent_child_joint,
    BiomechCoordinateSystem,
    Segment,
    check_biomech_consistency,
    joint_string_to_enum,
    euler_sequence_to_enum,
    biomech_direction_string_to_enum,
    biomech_origin_string_to_enum,
    segment_str_to_enum,
    get_segment_columns,
)


def load_confident_data(df: pd.DataFrame, print_warnings: bool = False)-> pd.DataFrame:
    """ Load the confident data from the dataset """

    tested_segments = [
        ["thorax_x", "thorax_y", "thorax_z", "thorax_origin"],
        ["humerus_x", "humerus_y", "humerus_z", "humerus_origin"],
        ["scapula_x", "scapula_y", "scapula_z", "scapula_origin"],
        ["clavicle_x", "clavicle_y", "clavicle_z", "clavicle_origin"],
    ]

    segment_is_isb = [
        "thorax_is_isb",
        "humerus_is_isb",
        "scapula_is_isb",
        "clavicle_is_isb",
    ]

    # create an empty dataframe
    df_confident = pd.DataFrame(columns=df.columns)

    for i, row in df.iterrows():
        # print(row.article_author_year)

        for segment, is_isb, segment_enum in zip(tested_segments, segment_is_isb, Segment):
            # print(segment)
            # if any of each is nan, skip
            if (
                    isinstance(row[segment[0]], float)
                    or isinstance(row[segment[1]], float)
                    or isinstance(row[segment[2]], float)
            ):
                if np.isnan(row[segment[0]]) or np.isnan(row[segment[1]]) or np.isnan(row[segment[2]]):
                    # print(segment, "is nan")
                    continue

            # build the coordinate system
            bsys = BiomechCoordinateSystem.from_biomech_directions(
                x=biomech_direction_string_to_enum(row[segment[0]]),
                y=biomech_direction_string_to_enum(row[segment[1]]),
                z=biomech_direction_string_to_enum(row[segment[2]]),
                origin=biomech_origin_string_to_enum(row[segment[3]]),
                segment=segment_enum,
            )

            # print("is segment coordinate system ISB :", bsys.is_isb_oriented())

            if not bsys.is_isb() == row[is_isb]:
                if print_warnings:
                    print("WARNING : inconsistency in the dataset")
                    print("-- ", row.article_author_year, " --")
                    print(segment[0][:-2])
                    print("detected ISB oriented:", bsys.is_isb_oriented())
                    print("detected ISB origin:", bsys.is_isb_origin(), bsys.origin)
                    print("detected ISB oriented + origin:", bsys.is_isb())
                    print("expected ISB:", row[is_isb])
                continue

        if not isinstance(row.euler_sequence, str) and (row.euler_sequence == "nan" or np.isnan(row.euler_sequence)):
            if print_warnings:
                print("WARNING : euler sequence is nan, for joint", row.joint, row.article_author_year)
            continue

        # build the coordinate system
        bjoint = Joint(
            joint_type=joint_string_to_enum(row.joint),
            euler_sequence=euler_sequence_to_enum(row.euler_sequence),
        )

        if not check_parent_child_joint(bjoint.joint_type, parent_name=row.parent, child_name=row.child):
            if print_warnings:
                print("WARNING : inconsistency in the dataset")
                print(row.joint, row.article_author_year)
                print("detected :", bjoint.joint_type)
                print("expected :", row.parent, row.child)
            continue

        parent_segment = segment_str_to_enum(row.parent)
        parent_columns = get_segment_columns(parent_segment)
        child_segment = segment_str_to_enum(row.child)
        child_columns = get_segment_columns(child_segment)

        usable, callback_function = check_biomech_consistency(
            parent_segment=BiomechCoordinateSystem.from_biomech_directions(
                x=biomech_direction_string_to_enum(row[parent_columns[0]]),
                y=biomech_direction_string_to_enum(row[parent_columns[1]]),
                z=biomech_direction_string_to_enum(row[parent_columns[2]]),
                origin=biomech_origin_string_to_enum(row[parent_columns[3]]),
                segment=parent_segment,
            ),
            child_segment=BiomechCoordinateSystem.from_biomech_directions(
                x=biomech_direction_string_to_enum(row[child_columns[0]]),
                y=biomech_direction_string_to_enum(row[child_columns[1]]),
                z=biomech_direction_string_to_enum(row[child_columns[2]]),
                origin=biomech_origin_string_to_enum(row[child_columns[3]]),
                segment=child_segment,
            ),
            joint=bjoint,
        )
        if not usable:
            continue

        # add the row to the dataframe
        df_confident = pd.concat([df_confident, row.to_frame().T], ignore_index=True)

    return df_confident


# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.CLEAN.value)
print(df.shape)
df = load_confident_data(df)
print(df.shape)
