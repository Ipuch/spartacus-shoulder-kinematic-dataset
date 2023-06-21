"""
This example shows how to convert a rotation matrix from one coordinate system to another.
The rotation matrix is computed from the axes of the ISB coordinate system.
The rotation matrix is then converted to Euler angles, and the axes are permuted to match the sequence of the ISB axes.
Then we try to retrieve the euler angles from the ISB axes, and we compare the results.
"""
from shoulder import CartesianAxis, Segment, BiomechCoordinateSystem, EulerSequence
import numpy as np
import biorbd


def mat_2_rotation(R: np.ndarray) -> biorbd.Rotation:
    """Convert a 3x3 matrix to a biorbd.Rotation"""
    return biorbd.Rotation(R[0, 0], R[0, 1], R[0, 2], R[1, 0], R[1, 1], R[1, 2], R[2, 0], R[2, 1], R[2, 2])


bsys_1 = BiomechCoordinateSystem(
    segment=Segment.HUMERUS,
    antero_posterior_axis=CartesianAxis.minusZ,
    infero_superior_axis=CartesianAxis.plusY,
    medio_lateral_axis=CartesianAxis.plusX,
    # antero_posterior_axis=CartesianAxis.plusX,
    # infero_superior_axis=CartesianAxis.plusY,
    # medio_lateral_axis=CartesianAxis.plusZ,
)
initial_sequence = "yzx"
sequence_wanted = "yxz"  # classic for sternoclavicular, acromioclavicular, and scapulothoracic joint

# we compute the rotation matrix from the axes, R_isb_local
R_isb_local = mat_2_rotation(bsys_1.get_rotation_matrix())
print(biorbd.Rotation.toEulerAngles(R_isb_local, "zxy").to_array())

# Let's build two rotation matrices R01 and R02, such that a_in_0 = R01 @ a_in_1 and b_in_0 = R02 @ b_in_2
# to emulate two segments with different orientations
R01 = biorbd.Rotation.fromEulerAngles(rot=np.array([0.1, 0.2, 0.3]), seq="zxy")
R02 = biorbd.Rotation.fromEulerAngles(rot=np.array([-0.09, -0.21, -0.301]), seq="zxy")

# compute the rotation matrix between the two
R12 = R01.to_array().transpose() @ R02.to_array()
print(R12)

# compute the euler angles of the rotation matrix with the sequence zxy
euler = biorbd.Rotation.toEulerAngles(mat_2_rotation(R12), initial_sequence).to_array()
print("euler angles")
print(euler)

# applied the rotation matrix R to R1 and R2
R01_rotated = R01.to_array() @ R_isb_local.to_array().transpose()
R02_rotated = R02.to_array() @ R_isb_local.to_array().transpose()

new_R = R01_rotated.transpose() @ R02_rotated
# compute the euler angles of the rotated matrices
euler1 = biorbd.Rotation.toEulerAngles(mat_2_rotation(new_R), sequence_wanted).to_array()
print("euler angles of new_R rotated")
print(euler1)

# check before if ratios are not too far from 1
print("ratios")
if not np.any(np.abs(euler1 / euler) < 0.999) and not np.any(np.abs(euler1 / euler) > 1.001):
    print("ratios are ok")
else:
    raise RuntimeError(f"ratios are too far from 1: {euler1 / euler}")

# find the signs to apply to the euler angles to get the same result as the previous computation
signs = np.sign(euler1 / euler)

print("conversion factors to apply to the euler angles are:")
print(signs)
