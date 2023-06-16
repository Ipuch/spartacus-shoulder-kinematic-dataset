import numpy as np
import pandas as pd

from .enums import JointType, Segment
from .utils import segment_str_to_enum, Joint, BiomechCoordinateSystem, get_is_isb_column


def check_parent_child_joint(bjoint: Joint, row: pd.Series, print_warnings: bool = False):
    """
    This function checks if the parent and child segment are compatible with the joint type.

    Parameters
    ----------
    bjoint : Joint
        The joint to check.
    row : pandas.Series
        The row of the dataset to check.
    print_warnings : bool, optional
        If True, print warnings when inconsistencies are found. The default is False.

    Returns
    -------
    bool
        True if the parent and child segment are compatible with the joint type, False otherwise.
    """
    if not _check_parent_child_joint(bjoint.joint_type, parent_name=row.parent, child_name=row.child):
        if print_warnings:
            print("WARNING : inconsistency in the dataset")
            print(row.joint, row.article_author_year)
            print("detected :", bjoint.joint_type)
            print("expected :", row.parent, row.child)
        return False
    return True


def _check_parent_child_joint(joint_type: JointType, parent_name: str, child_name: str) -> bool:
    parent_segment = segment_str_to_enum(parent_name)
    child_segment = segment_str_to_enum(child_name)

    if joint_type == JointType.GLENO_HUMERAL:
        # Scapula is the parent segment of the humerus
        return parent_segment == Segment.SCAPULA and child_segment == Segment.HUMERUS
    elif joint_type == JointType.ACROMIO_CLAVICULAR:
        # Clavicle is the parent segment of the scapula
        return parent_segment == Segment.CLAVICLE and child_segment == Segment.SCAPULA
    elif joint_type == JointType.STERNO_CLAVICULAR:
        # Clavicle is the parent segment of the thorax
        return parent_segment == Segment.THORAX and child_segment == Segment.CLAVICLE
    elif joint_type == JointType.THORACO_HUMERAL:
        # Thorax is the parent segment of the humerus
        return parent_segment == Segment.THORAX and child_segment == Segment.HUMERUS
    elif joint_type == JointType.SCAPULO_THORACIC:
        # Thorax is the parent segment of the scapula
        return parent_segment == Segment.THORAX and child_segment == Segment.SCAPULA
    else:
        raise ValueError(f"{joint_type} is not a valid joint type.")


def check_segment_filled_with_nan(row: pd.Series, segment: list, print_warnings: bool = False):
    """
    This function checks if the segment is not given and filled with NaN values.

    Parameters
    ----------
    row : pandas.Series
        The row of the dataset to check.
    segment : list
        The list of the columns of the segment to check. e.g. ["humerus_x", "humerus_y", "humerus_z"]
    print_warnings : bool, optional
        If True, print warnings when inconsistencies are found. The default is False.

    Returns
    -------
    bool
        True if the segment is filled with NaN values, False otherwise.
    """
    if isinstance(row[segment[0]], float) or isinstance(row[segment[1]], float) or isinstance(row[segment[2]], float):
        if np.isnan(row[segment[0]]) or np.isnan(row[segment[1]]) or np.isnan(row[segment[2]]):
            if print_warnings:
                print(segment, " is filled with nan")
            return True
    return False


def check_is_isb_segment(row: pd.Series, bsys: BiomechCoordinateSystem, print_warnings: bool = False) -> bool:
    """
    This function checks if the segment is ISB oriented and if it is well specified in the dataset.

    Parameters
    ----------
    bsys : BiomechCoordinateSystem
        The biomechanical coordinate system to check.
    row : pandas.Series
        The row of the dataset to check.
    print_warnings : bool, optional
        If True, print warnings when inconsistencies are found. The default is False.

    Returns
    -------
    bool
        True if the segment is ISB oriented and if it is well specified in the dataset, False otherwise.
    """
    is_isb = get_is_isb_column(bsys.segment)

    if not bsys.is_isb() == row[is_isb]:
        if print_warnings:
            print("WARNING : inconsistency in the dataset")
            print("-- ", row.article_author_year, " --")
            print(bsys.segment)
            print("detected ISB oriented:", bsys.is_isb_oriented())
            print("detected ISB origin:", bsys.is_isb_origin(), bsys.origin)
            print("detected ISB oriented + origin:", bsys.is_isb())
            print("expected ISB:", row[is_isb])
        return False

    return True


def check_is_euler_sequence_provided(row: pd.Series, print_warnings: bool = False) -> bool:
    """This function checks if the euler sequence is provided in the dataset."""
    if not isinstance(row.euler_sequence, str) and (row.euler_sequence == "nan" or np.isnan(row.euler_sequence)):
        if print_warnings:
            print("WARNING : euler sequence is nan, for joint", row.joint, row.article_author_year)
        return False
    # check the three letters
    if not len(row.euler_sequence) == 3:
        if print_warnings:
            print("WARNING : euler sequence is not 3 letters long, for joint", row.joint, row.article_author_year)
        return False
    # check if the letters are x, y, or z
    authorized_letters = ["x", "y", "z"]
    if (
        not row.euler_sequence[0] in authorized_letters
        or not row.euler_sequence[1] in authorized_letters
        or not row.euler_sequence[2] in authorized_letters
    ):
        if print_warnings:
            print("WARNING : euler sequence is not x, y, or z, for joint", row.joint, row.article_author_year)
        return False

    return True


def check_same_orientation(parent: BiomechCoordinateSystem, child: BiomechCoordinateSystem, print_warnings: bool = False) -> bool:
    """ This function checks if the parent and child segments have the same orientation."""
    condition1 = parent.anterior_posterior_axis == child.anterior_posterior_axis
    condition2 = parent.medio_lateral_axis == child.medio_lateral_axis
    condition3 = parent.infero_superior_axis == child.infero_superior_axis

    output = True
    if not condition1 or not condition2 or not condition3:
        if print_warnings:
            print("WARNING : inconsistency in the dataset")
            print("parent :", parent.segment, parent.anterior_posterior_axis, parent.medio_lateral_axis, parent.infero_superior_axis)
            print("child :", child.segment, child.anterior_posterior_axis, child.medio_lateral_axis, child.infero_superior_axis)
        output = False

    return output


def check_is_translation_provided(row: pd.Series, print_warnings: bool = False) -> bool:
    """ This function checks if the translation is provided in the dataset."""
    # check that the column origin_displacement and displacement_cs (coordinate system) are not nan

    origin_displacement_provided = isinstance(row.origin_displacement, str) and (not row.origin_displacement == "nan" or not np.isnan(row.origin_displacement))
    displacement_cs_provided = isinstance(row.displacement_cs, str) and (not row.displacement_cs == "nan" or not np.isnan(row.displacement_cs))

    if not (origin_displacement_provided and not displacement_cs_provided):
        if print_warnings:
            print("WARNING : translation is not entirely provided, for joint", row.joint, row.article_author_year)
            print(f"origin_displacement_provided : {origin_displacement_provided}")
            print(f"displacement_cs_provided : {displacement_cs_provided}")
        return False
    return True