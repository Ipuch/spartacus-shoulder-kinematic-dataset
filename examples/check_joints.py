import pandas as pd
import numpy as np

from shoulder import DatasetCSV, Joint, joint_string_to_enum, euler_sequence_to_enum, check_parent_child_joint

# open the file only_dataset_raw.csv
df = pd.read_csv(DatasetCSV.CLEAN.value)
# for each row verify the ISB convention
for i, row in df.iterrows():
    if not isinstance(row.euler_sequence, str) and (row.euler_sequence == "nan" or np.isnan(row.euler_sequence)):
        print("WARNING : euler sequence is nan, for joint", row.joint, row.article_author_year)
        continue

    # build the coordinate system
    bjoint = Joint(
        joint_type=joint_string_to_enum(row.joint),
        euler_sequence=euler_sequence_to_enum(row.euler_sequence),
    )

    if not check_parent_child_joint(bjoint.joint_type, parent_name=row.parent, child_name=row.child):
        print("WARNING : inconsistency in the dataset")
        print(row.joint, row.article_author_year)
        print("detected :", bjoint.joint_type)
        print("expected :", row.parent, row.child)
