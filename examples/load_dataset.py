import pandas as pd
import numpy as np

from shoulder import DatasetCSV, biomech_direction_string_to_enum, BiomechCoordinateSystem

# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.CLEAN.value)
# for each row verify the ISB convention
for i, row in df.iterrows():

    print(row.article_author_year)

    tested_segments = [
        ["thorax_x", "thorax_y", "thorax_z"],
        ["humerus_x", "humerus_y", "humerus_z"],
        ["scapula_x", "scapula_y", "scapula_z"],
        ["clavicle_x", "clavicle_y", "clavicle_z"],
    ]

    for segment in tested_segments:
        print(segment)
        # if any of each is nan, skip
        if isinstance(row[segment[0]], float) or isinstance(row[segment[1]], float) or isinstance(
            row[segment[2]], float
        ):
            if np.isnan(row[segment[0]]) or np.isnan(row[segment[1]]) or np.isnan(row[segment[2]]):
                print(segment, "is nan")
                continue

        # build the coordinate system
        sys = BiomechCoordinateSystem.from_biomech_directions(
            x=biomech_direction_string_to_enum(row[segment[0]]),
            y=biomech_direction_string_to_enum(row[segment[1]]),
            z=biomech_direction_string_to_enum(row[segment[2]]),
        )
        print("is segment coordinate system ISB :", sys.is_isb())
