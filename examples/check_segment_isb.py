import pandas as pd
import numpy as np

from spartacus import (
    DatasetCSV,
    BiomechDirection,
    BiomechOrigin,
    BiomechCoordinateSystem,
    Segment,
)

# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.CLEAN.value)
# for each row verify the ISB convention
for i, row in df.iterrows():
    # print(row.article_author_year)

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
            x=BiomechDirection.from_string(row[segment[0]]),
            y=BiomechDirection.from_string(row[segment[1]]),
            z=BiomechDirection.from_string(row[segment[2]]),
            origin=BiomechOrigin.from_string(row[segment[3]]),
            segment=segment_enum,
        )

        # print("is segment coordinate system ISB :", bsys.is_isb_oriented())

        if not bsys.is_isb() == row[is_isb]:
            print("WARNING : inconsistency in the dataset")
            print("-- ", row.article_author_year, " --")
            print(segment[0][:-2])
            print("detected ISB oriented:", bsys.is_isb_oriented())
            print("detected ISB origin:", bsys.is_isb_origin(), bsys.origin)
            print("detected ISB oriented + origin:", bsys.is_isb())
            print("expected ISB:", row[is_isb])

# todo: does the origin defines the segment frame ?
#  if not, rotation can be used directly.
#  if yes, the origin as to be along ISB axis
# todo: if isb false, but a correction exists, it should be usable.
#
