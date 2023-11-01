import biorbd
import numpy as np

from .enums import Segment

def mat_2_rotation(R: np.ndarray) -> biorbd.Rotation:
    """Convert a 3x3 matrix to a biorbd.Rotation"""
    return biorbd.Rotation(R[0, 0], R[0, 1], R[0, 2], R[1, 0], R[1, 1], R[1, 2], R[2, 0], R[2, 1], R[2, 2])

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



# def check_biomech_consistency(
#     parent_segment: BiomechCoordinateSystem,
#     child_segment: BiomechCoordinateSystem,
#     joint: Joint,
# ) -> tuple[bool, callable]:
#     """
#     Check if the biomechanical coordinate system of the parent and child segment
#     are compatible with the joint type and ISB sequences
#
#     Parameters
#     ----------
#     parent_segment : BiomechCoordinateSystem
#         The parent segment coordinate system
#     child_segment : BiomechCoordinateSystem
#         The child segment coordinate system
#     joint : Joint
#         The joint type
#
#     Returns
#     -------
#     tuple(bool, callable)
#         bool
#             True if the biomechanical coordinate system is compatible with ISB
#         tuple
#             The conversion factor for dof1, dof2, dof3 of euler angles
#
#
#     """
#
#     parent_isb = parent_segment.is_isb_oriented()
#     child_isb = child_segment.is_isb_oriented()
#
#     if parent_isb and child_isb:
#         if joint.is_joint_sequence_isb():
#             return True, get_angle_conversion_callback_from_tuple((1, 1, 1))
#         else:
#             # rebuild the rotation matrix from angles and sequence and identify the ISB angles from the rotation matrix
#             return True, get_angle_conversion_callback_from_sequence(
#                 previous_sequence=joint.euler_sequence,
#                 new_sequence=get_isb_sequence_from_joint_type(joint_type=joint.joint_type),
#             )
#     elif not parent_isb or not child_isb:  # This is to isb correction !
#         # This should be a two-step process
#         # 1. Check if the two segments are oriented in the same direction
#         # 2. Convert the euler angles to get them such that the two segments are ISB oriented
#         # 3. Check if the previous joint angle sequence is compatible with the new ISB sequence
#         # 3.1. If yes, return the conversion factor
#         # 4. If not, change the isb sequence with get_angle_conversion_callback_from_sequence(...)
#         # it may not include the step where we check if the origin is on an isb axis, especially for the scapula, consider kolz conversion
#         # build the rotation matrix from the euler angles and sequence, applied kolz conversion to the rotation matrix
#         # identify again the euler angles from the rotation matrix
#         output = get_conversion_from_not_isb_to_isb_oriented(
#             parent_segment=parent_segment,
#             child_segment=child_segment,
#             joint=joint,
#         )
#         if output[0]:
#             return output[0], get_angle_conversion_callback_from_tuple(output[1])
#         else:
#             # return print("NotImplementedError: Check conversion not implemented yet")
#             return output[0], lambda rot1, rot2, rot3: (np.nan, np.nan, np.nan)
#     else:
#         raise NotImplementedError("Check conversion not implemented yet")


def get_segment_columns(segment: Segment) -> list[str]:
    columns = {
        Segment.THORAX: ["thorax_x", "thorax_y", "thorax_z", "thorax_origin"],
        Segment.CLAVICLE: ["clavicle_x", "clavicle_y", "clavicle_z", "clavicle_origin"],
        Segment.SCAPULA: ["scapula_x", "scapula_y", "scapula_z", "scapula_origin"],
        Segment.HUMERUS: ["humerus_x", "humerus_y", "humerus_z", "humerus_origin"]
    }
    return columns.get(segment, ValueError(f"{segment} is not a valid segment."))


def get_is_isb_column(segment: Segment) -> str:
    columns = {
        Segment.THORAX: "thorax_is_isb",
        Segment.CLAVICLE: "clavicle_is_isb",
        Segment.SCAPULA: "scapula_is_isb",
        Segment.HUMERUS: "humerus_is_isb"
    }
    return columns.get(segment, ValueError(f"{segment} is not a valid segment."))


def get_correction_column(segment: Segment) -> str:
    columns = {
        Segment.THORAX: "thorax_correction_method",
        Segment.CLAVICLE: "clavicle_correction_method",
        Segment.SCAPULA: "scapula_correction_method",
        Segment.HUMERUS: "humerus_correction_method"
    }
    return columns.get(segment, ValueError(f"{segment} is not a valid segment."))


def get_is_correctable_column(segment: Segment) -> str:
    columns = {
        Segment.THORAX: "thorax_is_isb_correctable",
        Segment.CLAVICLE: "clavicle_is_isb_correctable",
        Segment.SCAPULA: "scapula_is_isb_correctable",
        Segment.HUMERUS: "humerus_is_isb_correctable"
    }
    return columns.get(segment, ValueError(f"{segment} is not a valid segment."))


def compute_rotation_matrix_from_axes(
    anterior_posterior_axis: np.ndarray,
    infero_superior_axis: np.ndarray,
    medio_lateral_axis: np.ndarray,
):
    """
    Compute the rotation matrix from the axes of the ISB coordinate system, the rotation matrix from the axes,
    named R_isb_local such that v_isb = R_isb_local @ v_local

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
