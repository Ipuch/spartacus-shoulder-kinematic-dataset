"""
This example shows how to convert a rotation matrix from one coordinate system to another.
The rotation matrix is computed from the axes of the ISB coordinate system.
The rotation matrix is then converted to Euler angles, and the axes are permuted to match the sequence of the ISB axes.
Then we try to retrieve the euler angles from the ISB axes, and we compare the results.

"The title is broke your ISB intuition
but in fact it restored it for me" Pierre Puchaud.

"""
import numpy as np

# We can either do it with scipy or with biorbd
# Let's choose scipy as this is a more common toolbox
from scipy.spatial.transform import Rotation


# compute the rotation matrix from the axes, R_isb_local
def compute_rotation_matrix_from_axes(
    anterior_posterior_axis: np.ndarray,
    infero_superior_axis: np.ndarray,
    medio_lateral_axis: np.ndarray,
):
    """
    Compute the rotation matrix from the axes of the ISB coordinate system

    Parameters
    ----------
    anterior_posterior_axis: np.ndarray
        The anterior-posterior axis expressed in the ISB coordinate system
    infero_superior_axis: np.ndarray
        The infero-superior axis expressed in the ISB coordinate system
    medio_lateral_axis: np.ndarray
        The medio-lateral axis expressed in the ISB coordinate system

    Returns
    -------
    np.ndarray
        The rotation matrix from the ISB coordinate system to the local coordinate system
        R_isb_local
        meaning when a vector v expressed in local coordinates is transformed to ISB coordinates
        v_isb = R_isb_local @ v_local
    """
    return np.array(
        [
            # X axis                                    Y axis                                      Z axis ,
            #  in ISB base
            [
                anterior_posterior_axis[0, 0],
                infero_superior_axis[0, 0],
                medio_lateral_axis[0, 0],
            ],
            [
                anterior_posterior_axis[1, 0],
                infero_superior_axis[1, 0],
                medio_lateral_axis[1, 0],
            ],
            [
                anterior_posterior_axis[2, 0],
                infero_superior_axis[2, 0],
                medio_lateral_axis[2, 0],
            ],
        ],
        dtype=np.float64,
    ).T  # where the transpose was missing in the original code


def flip_rotations(angles: np.ndarray, seq: str) -> np.ndarray:
    """
    Return an alternate sequence with the second angle inverted, but that
        leads to the same rotation matrices. See below for more information.

    Parameters
    ----------
    angles: np.ndarray
        The rotation angles
    seq: str
        The sequence of the rotation angles

    Returns
    -------
    np.ndarray
        The rotation angles flipped


    Source
    ------
    github.com/felixchenier/kineticstoolkit/blob/24e3dd39a6546d475732b70609c07fcc26dc2ff7/kineticstoolkit/geometry.py#L526-L537

    Notes
    -----
    Before flipping, the angles are:

    - First angle belongs to [-180, 180] degrees (both inclusive)
    - Second angle belongs to:

        - [-90, 90] degrees if all axes are different. e.g., xyz
        - [0, 180] degrees if first and third axes are the same e.g., zxz

    - Third angle belongs to [-180, 180] degrees (both inclusive)

    If after flipping, the angles are:

    - First angle belongs to [-180, 180] degrees (both inclusive)
    - Second angle belongs to:

        - [-180, -90], [90, 180] degrees if all axes are different. e.g., xyz
        - [-180, 0] degrees if first and third axes are the same e.g., zxz

    - Third angle belongs to [-180, 180] degrees (both inclusive)
    """
    offset = np.pi  # only in radians

    if seq[0] == seq[2]:  # Euler angles
        angles[0] = np.mod(angles[0], 2 * offset) - offset
        angles[1] = -angles[1]
        angles[2] = np.mod(angles[2], 2 * offset) - offset
    else:  # Tait-Bryan angles
        angles[0] = np.mod(angles[0], 2 * offset) - offset
        angles[1] = offset - angles[1]
        angles[angles[1] > offset, :] -= 2 * offset
        angles[2] = np.mod(angles[2], 2 * offset) - offset

    return angles


# simplification for matlabists
X = np.array([1, 0, 0])[:, np.newaxis]  # (3 x 1)
Y = np.array([0, 1, 0])[:, np.newaxis]  # (3 x 1)
Z = np.array([0, 0, 1])[:, np.newaxis]  # (3 x 1)

R_isb_isb = compute_rotation_matrix_from_axes(
    anterior_posterior_axis=X,
    infero_superior_axis=Y,
    medio_lateral_axis=Z,
)

print("R_isb_isb: ", R_isb_isb)
print("It gives the identity matrix as expected, as no rotation is performed as the base is already ISB")

# Let's consider another local coordinate system, with the following axes
R_isb_local = compute_rotation_matrix_from_axes(
    anterior_posterior_axis=Y,
    infero_superior_axis=Z,
    medio_lateral_axis=X,
)
R_local_isb = R_isb_local.T

print("R_isb_local: ", R_isb_local)
print("We get some permutation of the identity matrix")

# The sequence of the data
bad_sequence = "zyx"

# classic for sternoclavicular, acromioclavicular, and scapulothoracic joint
isb_sequence = "yxz"

# the sequence that matches previous identify euler angles (not expected based on intuition)
matching_sequence = "xzy"

print("R_isb_local: ", R_isb_local)
print("R_local_isb: ", R_local_isb)

# Let's build two rotation matrices R01 and R02, such that :
# a_in_0 = R01 @ a_in_1 and,
# b_in_0 = R02 @ b_in_2
# to emulate two segments with different orientations
# NOTE: intrinsic rotation are in uppercase in scipy
R01 = Rotation.from_euler("ZXY", np.array([0.1, 0.2, 0.3])).as_matrix()
R02 = Rotation.from_euler("ZXY", np.array([-0.09, -0.21, -0.301])).as_matrix()

# compute the rotation matrix between the two
R12 = R01.transpose() @ R02
print(R12)

# compute the euler angles of the rotation matrix with the sequence zxy
euler_scipy = Rotation.from_matrix(R12).as_euler(bad_sequence.upper())
print("Scipy euler angles of R12: ")
print(euler_scipy)


# applied the rotation matrix R_isb_local to R1 and R2
# R01_rotated = R01 @ R_isb_local.transpose()    # R01 @ R1_1'   ' stands for isb
# R02_rotated = R02 @ R_isb_local.transpose()    # R02 @ R2_2'   ' stands for isb

new_R = R_isb_local @ R12 @ R_isb_local.transpose()
#  new_R = R1'2'  ' stands for isb coordinate systems
# R_isb_local = R1'1   ' stands for isb
# R_isb_local = R2'2   ' stands for isb

# compute the euler angles of the rotated matrices
new_euler_scipy = Rotation.from_matrix(new_R).as_euler(isb_sequence.upper())
print("Scipy euler angles of new_R rotated:")
print(new_euler_scipy)

# print the two rotation matrices next to each other
print("previous rotation matrix | new rotation matrix")
print(np.hstack((R12, new_R)))

# check before if ratios are not too far from 1
if np.all(np.abs(new_euler_scipy - euler_scipy) < 0.0001):
    print("ratios are ok")
else:
    from shoulder.utils import flip_rotations

    print("ratios are not ok, trying to flip the rotations")
    new_euler_flipped = flip_rotations(new_euler_scipy, isb_sequence)
    if np.all(np.abs(new_euler_flipped - euler_scipy) < 0.0001):
        print("ratios are ok after flipping")
    else:
        raise RuntimeError(f"ratios are too far from 1: {new_euler_scipy / euler_scipy}")

# find the signs to apply to the euler angles to get the same result as the previous computation
print()
print("signs: ", new_euler_scipy / euler_scipy)
signs = np.sign(new_euler_scipy / euler_scipy)

# extra check try to rebuild the rotation matrix from the initial euler angles and the sign factors
extra_R_from_initial_euler_and_factors = Rotation.from_euler(isb_sequence.upper(), euler_scipy * signs).as_matrix()

print("extra_R_from_initial_euler_and_factors: ")
print(extra_R_from_initial_euler_and_factors)
print("new_R: ")
print(new_R)


# supplementary check
R_init_bad = R_isb_local.transpose()
R_init_isb = R_isb_isb

Rqq_bad = Rotation.from_euler("xzy", np.array([0.1, 0.2, 0.3])).as_matrix()
Rqq_isb = Rotation.from_euler("xzy", np.array([0.1, 0.2, 0.3])).as_matrix()

rotated_Rqq_bad = R_init_bad @ Rqq_bad  # R01 R_0_bad
rotated_Rqq_isb = R_init_isb @ Rqq_isb  # R02 R_0_isb
