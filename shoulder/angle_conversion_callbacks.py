import biorbd
import numpy as np
from .enums import EulerSequence


def get_angle_conversion_callback_from_tuple(tuple_factors: tuple[int, int, int]) -> callable:
    if not all([x in [-1, 1] for x in tuple_factors]):
        raise ValueError("tuple_factors must be a tuple of 1 and -1")

    return lambda rot1, rot2, rot3: (
        rot1 * tuple_factors[0],
        rot2 * tuple_factors[1],
        rot3 * tuple_factors[2],
    )


def convert_euler_angles(previous_sequence_str: str, new_sequence_str: str, rot1, rot2, rot3) -> np.ndarray:
    """Convert Euler angles from one sequence to another"""
    r = biorbd.Rotation.fromEulerAngles(np.array([rot1, rot2, rot3]), seq=previous_sequence_str)
    return biorbd.Rotation.toEulerAngles(r, seq=new_sequence_str).to_array()


def get_angle_conversion_callback_from_sequence(previous_sequence: EulerSequence, new_sequence: EulerSequence):
    # check if sequences are different
    if previous_sequence == new_sequence:
        raise ValueError("previous_sequence and new_sequence must be different")

    previous_sequence_str = previous_sequence.value.lower()
    new_sequence_str = new_sequence.value.lower()
    return lambda rot1, rot2, rot3: convert_euler_angles(previous_sequence_str, new_sequence_str, rot1, rot2, rot3)
