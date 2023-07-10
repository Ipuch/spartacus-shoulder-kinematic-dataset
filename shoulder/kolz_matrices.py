import numpy as np
from .enums import Correction


def get_kolz_rotation_matrix(correction: Correction) -> np.ndarray:
    """
    This function returns the rotation matrix for the given correction.

    Parameters
    ----------
    correction : Correction
        The correction to apply.

    Source
    ------
    Kolz, C. W., Sulkar, H. J., Aliaj, K., Tashjian, R. Z., Chalmers, P. N., Qiu, Y., ... & Henninger, H. B. (2020).
    Reliable interpretation of scapular kinematics depends on coordinate system definition. Gait & posture, 81, 183-190.

    Returns
    -------
    np.ndarray
        The rotation matrix for the given correction.
        R_isb_local, such that a_in_isb = R_isb_local * a_in_local
    """

    if correction == Correction.SCAPULA_KOLZ_AC_TO_PA_ROTATION:
        # meaning a vector in AC coordinate system is expressed as:
        # a' = R * a
        # where a' is the vector expressed in the PA coordinate system
        return np.array(
            [
                [0.965, 0.010, -0.263],
                [-0.057, 0.984, 0.171],
                [0.257, 0.180, 0.950]
            ],
        ).T

    elif correction == Correction.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION:
        # meaning a vector in glenoid coordinate system is expressed as:
        # a' = R * a
        # where a' is the vector expressed in the PA coordinate system
        return np.array(
            [
                [0.949, 0.010, -0.314],
                [-0.056, 0.978, 0.200],
                [0.310, -0.208, 0.928],
            ],
        ).T

    else:
        raise ValueError(f"{correction} is not a valid correction. Only {Correction.SCAPULA_KOLZ_AC_TO_PA_ROTATION} "
                         f"and {Correction.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION} are valid corrections.")