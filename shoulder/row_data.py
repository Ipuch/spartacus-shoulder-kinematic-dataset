import numpy as np
import pandas as pd

from .enums import JointType, Segment
from .utils import (
    get_segment_columns,
    get_correction_column,
    BiomechCoordinateSystem,
    biomech_direction_string_to_enum,
    biomech_origin_string_to_enum,
    Joint,
    joint_string_to_enum,
    segment_str_to_enum,
    euler_sequence_to_enum,
    get_isb_sequence_from_joint_type,
    get_conversion_from_not_isb_to_isb_oriented,
    get_conversion_from_not_isb_to_isb_oriented_v2,
    convert_rotation_matrix_from_one_coordinate_system_to_another,
)

from .angle_conversion_callbacks import (
    get_angle_conversion_callback_from_tuple,
    get_angle_conversion_callback_from_sequence,
    get_angle_conversion_callback_to_isb_with_sequence,
)

from .checks import (
    check_segment_filled_with_nan,
    check_is_isb_segment,
    check_is_euler_sequence_provided,
    check_is_translation_provided,
    check_parent_child_joint,
    check_same_orientation,
)


class RowData:
    """
    This class is used to store the data of a row of the dataset and make it accessible through attributes and methods.
    """

    def __init__(self, row: pd.Series):
        """
        Parameters
        ----------
        row : pandas.Series
            The row of the dataset to store.
        """

        self.row = row

        self.joint = None

        self.parent_segment = segment_str_to_enum(self.row.parent)
        self.parent_columns = get_segment_columns(self.parent_segment)
        self.parent_biomech_sys = None

        self.child_segment = segment_str_to_enum(self.row.child)
        self.child_columns = get_segment_columns(self.child_segment)
        self.child_biomech_sys = None

        self.correction_callback = None
        self.usable_data = None

    def check_all_segments_validity(self, print_warnings: bool = False) -> bool:
        """
        Check all the segments of the row are valid.
        First, we check if the segment is provided, i.e., no NaN values.
        Second, we check if the segment defined as is_isb = True or False in the dataset
        and if the orientations of axis defined in the dataset fits with isb definition.

        (we don't mind if it's not a isb segment, we just don't want to have a segment
        that matches the is_isb given)

        Third, we check the frame are direct, det(R) = 1.

        Returns
        -------
        bool
            True if all the segments are valid, False otherwise.
        """
        output = True
        for segment_enum in Segment:
            segment_cols = get_segment_columns(segment_enum)
            # first check
            if check_segment_filled_with_nan(self.row, segment_cols, print_warnings=print_warnings):
                continue

            # build the coordinate system
            bsys = BiomechCoordinateSystem.from_biomech_directions(
                x=biomech_direction_string_to_enum(self.row[segment_cols[0]]),
                y=biomech_direction_string_to_enum(self.row[segment_cols[1]]),
                z=biomech_direction_string_to_enum(self.row[segment_cols[2]]),
                origin=biomech_origin_string_to_enum(self.row[segment_cols[3]]),
                segment=segment_enum,
            )
            # second check
            if not check_is_isb_segment(self.row, bsys, print_warnings=print_warnings):
                output = False

            # third check if the segment is direct or not
            if not bsys.is_direct():
                if print_warnings:
                    print(
                        f"{self.row.article_author_year}, "
                        f"Segment {segment_enum.value} is not direct, "
                        f"it should be !!!"
                    )
                output = False

        return output

    def check_joint_validity(self, print_warnings: bool = False) -> bool:
        """
        Check if the joint defined in the dataset is valid.
        We expect the joint to have a valid euler sequence, i.e., no NaN values., three letters and valid letters.
        If not we expect the joint to have a valid translation, i.e., no NaN values.

        We expect the joint to have good parent and child definitions
        We expect the joint to have defined parent and child segments, i.e., no NaN values.

        Returns
        -------
        bool
            True if the joint is valid, False otherwise.
        """
        output = True

        no_euler_sequence = not check_is_euler_sequence_provided(self.row, print_warnings=print_warnings)
        no_translation = not check_is_translation_provided(self.row, print_warnings=print_warnings)

        if no_euler_sequence and no_translation:
            output = False
            if print_warnings:
                print(
                    f"Joint {self.row.joint} has no euler sequence defined, "
                    f" and no translation defined, "
                    f"it should not be empty !!!"
                )
            return output

        print(self.row.displacement_cs)
        if self.row.displacement_cs == 'nan':
            print('nan')

        self.joint = Joint(
            joint_type=joint_string_to_enum(self.row.joint),
            euler_sequence=euler_sequence_to_enum(self.row.euler_sequence),
            translation_origin=biomech_origin_string_to_enum(self.row.origin_displacement) if not no_translation else None,
            translation_frame=segment_str_to_enum(self.row.displacement_cs) if not no_translation else None,
        )

        if not check_parent_child_joint(self.joint, row=self.row, print_warnings=print_warnings):
            output = False

        # check database if nan in one the segment of the joint
        if check_segment_filled_with_nan(self.row, self.parent_columns, print_warnings=print_warnings):
            output = False
            if print_warnings:
                print(
                    f"Joint {self.row.joint} has a NaN value in the parent segment {self.row.parent}, "
                    f"it should not be empty !!!"
                )

        if check_segment_filled_with_nan(self.row, self.child_columns, print_warnings=print_warnings):
            output = False
            if print_warnings:
                print(
                    f"Joint {self.row.joint} has a NaN value in the child segment {self.row.child}, "
                    f"it should not be empty !!!"
                )

        return output

    def set_segments(self):
        """
        Set the parent and child segments of the joint.
        """

        self.parent_biomech_sys = BiomechCoordinateSystem.from_biomech_directions(
            x=biomech_direction_string_to_enum(self.row[self.parent_columns[0]]),
            y=biomech_direction_string_to_enum(self.row[self.parent_columns[1]]),
            z=biomech_direction_string_to_enum(self.row[self.parent_columns[2]]),
            origin=biomech_origin_string_to_enum(self.row[self.parent_columns[3]]),
            segment=self.parent_segment,
        )
        self.child_biomech_sys = BiomechCoordinateSystem.from_biomech_directions(
            x=biomech_direction_string_to_enum(self.row[self.child_columns[0]]),
            y=biomech_direction_string_to_enum(self.row[self.child_columns[1]]),
            z=biomech_direction_string_to_enum(self.row[self.child_columns[2]]),
            origin=biomech_origin_string_to_enum(self.row[self.child_columns[3]]),
            segment=self.child_segment,
        )

    def check_correction_validity(self, print_warnings: bool = False) -> bool:
        """
        We expect the correction columns to be filled with valid values.
        ex: if both segment are not isb, we expect the correction to_isb to be filled
        ex: if both segment are isb, we expect no correction to be filled
        ex: if both segment are isb, and euler sequence is isb, we expect no correction to be filled
        ex: if both segment are isb, and euler sequence is not isb, we expect the correction to_isb to be filled
        etc...

        """
        output = True

        parent_correction_column = get_correction_column(self.parent_segment)
        child_correction_column = get_correction_column(self.child_segment)

        # if both segments are isb, we expect no correction to be filled
        if self.parent_biomech_sys.is_isb() and self.child_biomech_sys.is_isb():
            correction_cell = self.row[parent_correction_column]
            if isinstance(correction_cell, str) and not (correction_cell == "nan" or np.isnan(correction_cell)):
                output = False
                if print_warnings:
                    print(
                        f"Joint {self.row.joint} has a correction value in the parent segment {self.row.parent}, "
                        f"it should be empty !!!, because the segment is isb. Current value: {correction_cell}"
                    )

            correction_cell = self.row[child_correction_column]
            if isinstance(correction_cell, str) and not (correction_cell == "nan" or np.isnan(correction_cell)):
                output = False
                if print_warnings:
                    print(
                        f"Joint {self.row.joint} has a correction value in the child segment {self.row.child}, "
                        f"it should be empty !!!, because the segment is isb. Current value: {correction_cell}"
                    )

            # # todo: not sure if it's relevant to save.
            # if self.joint.is_joint_sequence_isb():
            #     self.correction_on_euler_sequence = False
            # else:
            #     self.correction_on_euler_sequence = True

        # if both segments are not isb, we expect the correction to_isb to be filled
        if not self.parent_biomech_sys.is_isb():
            correction_cell = self.row[parent_correction_column]
            if not isinstance(correction_cell, str) and (correction_cell == "nan" or np.isnan(correction_cell)):
                output = False
                if print_warnings:
                    print(
                        f"Joint {self.row.joint} has no correction value in the parent segment {self.row.parent}, "
                        f"it should be filled !!!, because the segment is not isb. Current value: {correction_cell}"
                    )

        if not self.child_biomech_sys.is_isb():
            correction_cell = self.row[child_correction_column]
            # check if the check is well done.
            if not isinstance(correction_cell, str) and (correction_cell == "nan" or np.isnan(correction_cell)):
                output = False
                if print_warnings:
                    print(
                        f"Joint {self.row.joint} has no correction value in the child segment {self.row.child}, "
                        f"it should be filled !!!, because the segment is not isb. Current value: {correction_cell}"
                    )

        return output

    def set_correction_callback(self):
        """
        Set the correction callback of the joint.

        """
        parent_isb = self.parent_biomech_sys.is_isb_oriented()
        child_isb = self.child_biomech_sys.is_isb_oriented()

        if parent_isb and child_isb:
            if self.joint.is_joint_sequence_isb():
                self.usable_data = True
                self.correction_callback = get_angle_conversion_callback_from_tuple((1, 1, 1))
            else:
                # -- TO ISB SEQUENCE --
                # rebuild the rotation matrix from angles and sequence and identify the ISB angles from the rotation matrix
                self.usable_data = True
                self.correction_callback = get_angle_conversion_callback_from_sequence(
                    previous_sequence=self.joint.euler_sequence,
                    new_sequence=self.joint.isb_euler_sequence(),
                )

        elif not parent_isb or not child_isb:  # This is to isb correction !
            # 1. Check if the two segments are oriented in the same direction
            if not check_same_orientation(parent=self.parent_biomech_sys, child=self.child_biomech_sys):
                # todo: i don't know yet if useful
                self.usable_data = False
                self.correction_callback = None
                raise NotImplementedError("Not implemented yet, I don't know what to do yet.")

            # 2.If they are the same orientation,
            # convert the euler angles to get them such that the two segments are ISB oriented
            # NOTE: we don't actually convert the coordinate systems, we just convert the euler angles
            # Deprecated
            # output = get_conversion_from_not_isb_to_isb_oriented(
            #     parent=self.parent_biomech_sys,
            #     child=self.child_biomech_sys,
            #     joint=self.joint,
            # )
            # New method
            if self.joint.is_sequence_convertible_through_factors(print_warning=True):
                # output = get_conversion_from_not_isb_to_isb_oriented_v2(
                #     parent=self.parent_biomech_sys,
                #     child=self.child_biomech_sys,
                #     joint=self.joint,
                # )

                self.usable_data = True
                self.correction_callback = get_angle_conversion_callback_from_tuple(
                    convert_rotation_matrix_from_one_coordinate_system_to_another(
                        bsys=self.parent_biomech_sys,
                        initial_sequence=self.joint.euler_sequence,
                        sequence_wanted=self.joint.isb_euler_sequence(),
                    )
                )
            else:
                self.usable_data = True
                self.correction_callback = get_angle_conversion_callback_to_isb_with_sequence(
                    previous_sequence=self.joint.euler_sequence,
                    new_sequence=self.joint.isb_euler_sequence(),
                    bsys_child=self.child_biomech_sys,
                    bsys_parent=self.parent_biomech_sys,
                )

            # it may not include the step where we check if the origin is on an isb axis, especially for the scapula, consider kolz conversion
            # build the rotation matrix from the euler angles and sequence, applied kolz conversion to the rotation matrix
            # identify again the euler angles from the rotation matrix

        else:
            raise NotImplementedError("Check conversion not implemented yet")
