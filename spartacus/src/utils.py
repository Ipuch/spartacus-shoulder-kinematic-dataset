import biorbd
import numpy as np

from .enums import CartesianAxis, EulerSequence, JointType, BiomechDirection, BiomechOrigin, Segment, Correction
from .kolz_matrices import get_kolz_rotation_matrix


class BiomechCoordinateSystem:
    def __init__(
        self,
        segment: Segment,
        antero_posterior_axis: CartesianAxis,
        infero_superior_axis: CartesianAxis,
        medio_lateral_axis: CartesianAxis,
        origin=None,
    ):
        # verify isinstance
        if not isinstance(antero_posterior_axis, CartesianAxis):
            raise TypeError("antero_posterior_axis should be of type CartesianAxis")
        if not isinstance(infero_superior_axis, CartesianAxis):
            raise TypeError("infero_superior_axis should be of type CartesianAxis")
        if not isinstance(medio_lateral_axis, CartesianAxis):
            raise TypeError("medio_lateral_axis should be of type CartesianAxis")
        # verity they are all different
        if (
            antero_posterior_axis == infero_superior_axis
            or antero_posterior_axis == medio_lateral_axis
            or infero_superior_axis == medio_lateral_axis
        ):
            raise ValueError("antero_posterior_axis, infero_superior_axis, medio_lateral_axis should be different")

        self.anterior_posterior_axis = antero_posterior_axis
        self.infero_superior_axis = infero_superior_axis
        self.medio_lateral_axis = medio_lateral_axis

        self.origin = origin
        self.segment = segment

    @classmethod
    def from_biomech_directions(
        cls,
        x: BiomechDirection,
        y: BiomechDirection,
        z: BiomechDirection,
        origin: BiomechOrigin = None,
        segment: Segment = None,
    ):
        my_arg = dict()

        # verify each of the x, y, z is different
        if x == y or x == z or y == z:
            raise ValueError("x, y, z should be different")

        # verify is positive or negative
        actual_axes = [x, y, z]
        positive_enums_axis = [CartesianAxis.plusX, CartesianAxis.plusY, CartesianAxis.plusZ]
        negative_enums_axis = [CartesianAxis.minusX, CartesianAxis.minusY, CartesianAxis.minusZ]

        for axis, positive_enum, negative_enum in zip(actual_axes, positive_enums_axis, negative_enums_axis):
            if axis.sign == 1:
                if axis == BiomechDirection.PlusPosteroAnterior:
                    my_arg["antero_posterior_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusMedioLateral:
                    my_arg["medio_lateral_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusInferoSuperior:
                    my_arg["infero_superior_axis"] = positive_enum
                    continue
            elif axis.sign == -1:
                if axis == BiomechDirection.MinusPosteroAnterior:
                    my_arg["antero_posterior_axis"] = negative_enum
                    continue
                elif axis == BiomechDirection.MinusMedioLateral:
                    my_arg["medio_lateral_axis"] = negative_enum
                    continue
                elif axis == BiomechDirection.MinusInferoSuperior:
                    my_arg["infero_superior_axis"] = negative_enum
                    continue

        my_arg["origin"] = origin
        my_arg["segment"] = segment

        return cls(**my_arg)

    def is_isb_origin(self) -> bool:
        if self.segment == Segment.THORAX and self.origin == BiomechOrigin.Thorax.IJ:
            return True
        elif self.segment == Segment.CLAVICLE and self.origin == BiomechOrigin.Clavicle.STERNOCLAVICULAR_JOINT_CENTER:
            return True
        elif self.segment == Segment.SCAPULA and self.origin == BiomechOrigin.Scapula.ANGULAR_ACROMIALIS:
            return True
        elif self.segment == Segment.HUMERUS and self.origin == BiomechOrigin.Humerus.GLENOHUMERAL_HEAD:
            return True
        else:
            return False

    def is_origin_on_an_isb_axis(self) -> bool:
        """
        Return True if the origin is on an ISB axis, False otherwise

        NOTE
        ----
        The true definition would be, the origin is part of the process to build an ISB axis.

        """
        if self.is_isb_origin():
            return True

        if self.segment == Segment.THORAX:
            if self.origin == BiomechOrigin.Thorax.C7:
                return True
            elif self.origin == BiomechOrigin.Thorax.T8:
                return True
            elif self.origin == BiomechOrigin.Thorax.PX:
                return True
            else:
                return False

        if self.segment == Segment.CLAVICLE:
            if self.origin == BiomechOrigin.Clavicle.STERNOCLAVICULAR_JOINT_CENTER:
                return True
            elif self.origin == BiomechOrigin.Clavicle.ACROMIOCLAVICULAR_JOINT_CENTER:
                return True
            else:
                return False

        if self.segment == Segment.SCAPULA:
            if self.origin == BiomechOrigin.Scapula.TRIGNONUM_SPINAE:
                return True
            elif self.origin == BiomechOrigin.Scapula.ANGULUS_INFERIOR:
                return True
            else:
                return False

        if self.segment == Segment.HUMERUS:
            if self.origin == BiomechOrigin.Humerus.MIDPOINT_EPICONDYLES:
                return True
            else:
                return False

    def is_isb(self) -> bool:
        return self.is_isb_oriented() and self.is_isb_origin()

    def is_isb_oriented(self) -> bool:
        condition_1 = self.anterior_posterior_axis is CartesianAxis.plusX
        condition_2 = self.infero_superior_axis is CartesianAxis.plusY
        condition_3 = self.medio_lateral_axis is CartesianAxis.plusZ
        return condition_1 and condition_2 and condition_3

    def is_direct(self) -> bool:
        """check if the frame is direct (True) or indirect (False)"""
        return np.linalg.det(self.get_rotation_matrix()) > 0

    def get_rotation_matrix(self):
        """
        write the rotation matrix from the cartesian axis

        such that a_in_isb = R_to_isb_from_local @ a_in_local

        """

        # # find X axis in the cartesian axis
        # x_in_global =

        return np.array(
            [
                # X axis                                    Y axis                                      Z axis ,
                #  in ISB base
                [
                    self.anterior_posterior_axis.value[1][0],
                    self.infero_superior_axis.value[1][0],
                    self.medio_lateral_axis.value[1][0],
                ],
                [
                    self.anterior_posterior_axis.value[1][1],
                    self.infero_superior_axis.value[1][1],
                    self.medio_lateral_axis.value[1][1],
                ],
                [
                    self.anterior_posterior_axis.value[1][2],
                    self.infero_superior_axis.value[1][2],
                    self.medio_lateral_axis.value[1][2],
                ],
            ],
            dtype=np.float64,
        ).T

    def __print__(self):
        print(f"Segment: {self.segment}")
        print(f"Origin: {self.origin}")
        print(f"Anterior Posterior Axis: {self.anterior_posterior_axis}")
        print(f"Medio Lateral Axis: {self.medio_lateral_axis}")
        print(f"Infero Superior Axis: {self.infero_superior_axis}")


class Joint:
    def __init__(
        self,
        joint_type: JointType,
        euler_sequence: EulerSequence,
        translation_origin: BiomechOrigin,
        translation_frame: Segment,
    ):
        self.joint_type = joint_type
        self.euler_sequence = euler_sequence
        self.translation_origin = translation_origin
        self.translation_frame = translation_frame

    def is_joint_sequence_isb(self) -> bool:
        return EulerSequence.isb_from_joint_type(self.joint_type) == self.euler_sequence

    def isb_euler_sequence(self) -> EulerSequence:
        return EulerSequence.isb_from_joint_type(self.joint_type)

    # todo: stuff for translations ..?

    def is_sequence_convertible_through_factors(self, print_warning: bool = False) -> bool:
        """
        Check if the euler sequence of the joint can be converted to the ISB sequence with factors 1 or -1

        We expect the euler sequence to have three different letters, if the ISB sequence is YXZ (steroclavicular, acromioclavicular, scapulothoracic)
        We expect the euler sequence to have two different letters, if the ISB sequence is YXY (glenohumeral, thoracohumeral)

        Return
        ------
        bool
            True if the sequence can be converted with factors 1 or -1, False otherwise
        """
        if self.joint_type in (JointType.STERNO_CLAVICULAR, JointType.ACROMIO_CLAVICULAR, JointType.SCAPULO_THORACIC):
            sequence_wanted = EulerSequence.YXZ
            # check that we have three different letters in the sequence
            if len(set(self.euler_sequence.value)) != 3:
                if print_warning:
                    print(
                        "The euler sequence of the joint must have three different letters to be able to convert with factors 1"
                        f"or -1 to the ISB sequence {sequence_wanted.value}, but the sequence of the joint is"
                        f" {self.euler_sequence.value}"
                    )
                return False

        elif self.joint_type in (JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL):
            sequence_wanted = EulerSequence.YXY
            # check that the sequence in joint.euler_sequence as the same two letters for the first and third rotations
            if self.euler_sequence.value[0] != self.euler_sequence.value[2]:
                if print_warning:
                    print(
                        "The euler sequence of the joint must have the same two letters for the first and third rotations"
                        f"to be able to convert with factors 1 or -1 to the ISB sequence {sequence_wanted.value},"
                        f" but the sequence of the joint is {self.euler_sequence.value}"
                    )
                return False
        else:
            if print_warning:
                print(
                    "The joint type must be JointType.STERNO_CLAVICULAR, JointType.ACROMIO_CLAVICULAR,"
                    "JointType.SCAPULO_THORACIC, JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL"
                )
            return False

        return True


def get_conversion_from_not_isb_to_isb_oriented(
    parent: BiomechCoordinateSystem,
    child: BiomechCoordinateSystem,
    joint: Joint,
) -> tuple[bool, tuple[int, int, int]]:
    """
    Check if the combination of the coordinates and the euler sequence is valid to be used, according to the ISB

    Parameters
    ----------
    parent_segment : BiomechCoordinateSystem
        The parent segment
    child_segment : BiomechCoordinateSystem
        The child segment
    joint : Joint
        The joint

    Returns
    -------
    tuple[bool, tuple[int,int,int]]
        usable : bool
            True if the combination is valid, False otherwise
        tuple[int,int,int]
            Sign to apply to the dataset to make it compatible with the ISB

    """

    # create an empty list of 7 element
    condition = [None] * 7
    # all the joints have the same rotation sequence for the ISB YXZ
    if joint.joint_type in (JointType.STERNO_CLAVICULAR, JointType.ACROMIO_CLAVICULAR, JointType.SCAPULO_THORACIC):
        # rotation -90° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusY
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=z, x=x, z=-y")
            return True, (-1, 1, 1)

        # rotation 180° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-y, x=x, z=-z")
            return True, (-1, 1, -1)

        # rotation -270° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusY
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-z, x=x, z=y")
            return True, (1, 1, -1)

        # Rotation -90° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusZ
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusX
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusZ
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusX
        condition[6] = joint.euler_sequence == EulerSequence.YZX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=-z, z=x")
            return True, (1, -1, 1)

        # Rotation 180° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=-x, z=-z")
            return True, (1, -1, -1)

        # Rotation -270° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusZ
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusX
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusZ
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusX
        condition[6] = joint.euler_sequence == EulerSequence.YZX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=z, z=-x")
            return True, (1, 1, -1)

        # Rotation 90° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusY
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusX
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusY
        condition[4] = child.infero_superior_axis == CartesianAxis.plusX
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=x, x=-y, z=z")
            return True, (1, -1, 1)

        # Rotation -90° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusY
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusX
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusY
        condition[4] = child.infero_superior_axis == CartesianAxis.minusX
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-x, x=y, z=z")
            return True, (-1, 1, 1)

        # Rotation 180° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-y, x=-x, z=z")
            return True, (-1, -1, 1)

        # combined rotations +180 along z and +90 along x
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusY
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=z, x=-x, z=y")
            return True, (1, -1, 1)

        # combined rotations +90 along x and +90 along y
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusY
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusX
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusY
        condition[4] = child.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusX
        condition[6] = joint.euler_sequence == EulerSequence.ZYX

        if all(condition):
            # surprisingly this give the same angles, no sign change
            print("This is a valid combination, of the ISB sequence YXZ." "y=z, x=y, z=x")
            return True, (1, 1, 1)

        print("This is not a valid combination, of the ISB sequence YXZ.")
        return False, (0, 0, 0)

    # all the joints have the same rotation sequence for the ISB YXY
    elif joint.joint_type in (JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL):
        # Rotation -90° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusY
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=z, x=x, y=z")
            return True, (1, 1, 1)

        # Rotation 90° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusZ
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusY
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusZ
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-z, x=x, y=-z")
            return True, (-1, 1, -1)

        # Rotation 180° along X for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-y, x=x, y=-y")
            return True, (-1, 1, -1)

        # Rotation -90° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusZ
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusX
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusZ
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusX
        condition[6] = joint.euler_sequence == EulerSequence.YZY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=-z, y=y")
            return True, (1, -1, 1)

        # Rotation 90° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusZ
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusX
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusZ
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusX
        condition[6] = joint.euler_sequence == EulerSequence.YZY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=z, y=y")
            return True, (1, 1, 1)

        # Rotation 180° along Y for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=-x, y=y")
            return True, (1, -1, 1)

        # Rotation -90° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.plusY
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusX
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.plusY
        condition[4] = child.infero_superior_axis == CartesianAxis.minusX
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-x, x=y, y=-x")
            return True, (-1, 1, -1)

        # Rotation 90° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusY
        condition[1] = parent.infero_superior_axis == CartesianAxis.plusX
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusY
        condition[4] = child.infero_superior_axis == CartesianAxis.plusX
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=x, x=-y, y=x")
            return True, (1, -1, 1)

        # Rotation 180° along Z for each segment coordinate system
        condition[0] = parent.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-y, x=-x, y=-y")
            return True, (-1, -1, -1)

        return False, (0, 0, 0)

    else:
        raise ValueError(
            "The JointType is not supported. Please use:"
            "JointType.GLENO_HUMERAL, JointType.ACROMIO_CLAVICULAR,"
            "JointType.STERNO_CLAVICULAR, JointType.THORACO_HUMERAL,"
            "or JointType.SCAPULO_THORACIC"
        )


def mat_2_rotation(R: np.ndarray) -> biorbd.Rotation:
    """Convert a 3x3 matrix to a biorbd.Rotation"""
    return biorbd.Rotation(R[0, 0], R[0, 1], R[0, 2], R[1, 0], R[1, 1], R[1, 2], R[2, 0], R[2, 1], R[2, 2])


def convert_rotation_matrix_from_one_coordinate_system_to_another(
    bsys: BiomechCoordinateSystem,
    initial_sequence: EulerSequence,
    sequence_wanted: EulerSequence,
    child_extra_correction: Correction = None,
    parent_extra_correction: Correction = None,
) -> tuple[bool, tuple[int, int, int]]:
    """
    This function converts the current euler angles into a desired euler sequence.

    Parameters
    ----------
    bsys: BiomechCoordinateSystem
        The biomechanical coordinate system of the segment
    initial_sequence: EulerSequence
        The euler sequence of the rotation matrix
    sequence_wanted: EulerSequence
        The euler sequence of the rotation matrix wanted, e.g. ISB sequence
    child_extra_correction: Correction
        The correction to apply to the child segment
    parent_extra_correction: Correction
        The correction to apply to the parent segment

    Returns
    -------
    bool
        Whether the conversion is possible with sign factors
    tuple[int, int, int]
        The sign factors to apply to the euler angles to get the desired euler sequence
    """
    initial_sequence = initial_sequence.value
    sequence_wanted = sequence_wanted.value  # most of the time, it will be the ISB sequence

    R_isb_local = mat_2_rotation(bsys.get_rotation_matrix()).to_array()

    # Let's build two rotation matrices R01 and R02, such that a_in_0 = R01 @ a_in_1 and b_in_0 = R02 @ b_in_2
    # to emulate two segments with different orientations
    R01 = biorbd.Rotation.fromEulerAngles(rot=np.array([0.5, -0.8, 1.2]), seq="zxy").to_array()  # random values
    R02 = biorbd.Rotation.fromEulerAngles(rot=np.array([-0.01, 0.02, -0.03]), seq="zxy").to_array()  # ra

    # compute the rotation matrix between the two
    R12 = R01.transpose() @ R02
    # print(R12)

    # compute the euler angles of the rotation matrix with the sequence zxy
    euler = biorbd.Rotation.toEulerAngles(mat_2_rotation(R12), initial_sequence).to_array()
    # print("euler angles")
    # print(euler)
    # if we want to change if for scipy
    # euler_scipy = Rotation.from_matrix(R12).as_euler(bad_sequence.upper())

    # applied the rotation matrix R to R1 and R2
    #  ---  Deprecated --- not false but less generic
    # R01_rotated = R01 @ R_isb_local.transpose()
    # R02_rotated = R02 @ R_isb_local.transpose()
    # new_R = R01_rotated.transpose() @ R02_rotated
    #  ---  New way --- more generic
    # 1 : parent
    # 2 : child
    new_R = R_isb_local @ R12 @ R_isb_local.transpose()

    # extra corrections - Kolz
    if child_extra_correction is not None:
        print(f"I applied a correction of {child_extra_correction} to the child segment")
        R_child_correction = get_kolz_rotation_matrix(child_extra_correction, orthonormalize=True).T
        new_R = new_R @ R_child_correction

    if parent_extra_correction is not None:
        print(f"I applied a correction of {parent_extra_correction} to the parent segment")
        R_parent_correction = get_kolz_rotation_matrix(parent_extra_correction, orthonormalize=True)
        new_R = R_parent_correction @ new_R

    # compute the euler angles of the rotated matrices
    new_euler = biorbd.Rotation.toEulerAngles(mat_2_rotation(new_R), sequence_wanted).to_array()
    # print("euler angles of new_R rotated")
    # print(euler1)
    # if we want to change if for scipy
    # new_euler_scipy = Rotation.from_matrix(new_R).as_euler(isb_sequence.upper())

    # check before if ratios are not too far from 1
    ratio = new_euler / euler
    # check if the ratios with flipped euler angles are not too far from 1
    new_euler_flipped = flip_rotations(new_euler, sequence_wanted)
    ratio_flipped = new_euler_flipped / euler
    if not np.any(np.abs(ratio) < 0.999) and not np.any(np.abs(ratio) > 1.001):
        print("ratios are ok")
    elif not np.any(np.abs(ratio_flipped) < 0.999) and not np.any(np.abs(ratio_flipped) > 1.001):
        print("ratios are ok with flipped euler angles")
        new_euler = new_euler_flipped
    else:
        # raise RuntimeError(f"ratios are too far from 1: {ratio}")
        return False, (0, 0, 0)

    # find the signs to apply to the euler angles to get the same result as the previous computation
    signs = np.sign(ratio)

    # extra check try to rebuild the rotation matrix from the initial euler angles and the sign factors
    extra_R_from_initial_euler_and_factors = biorbd.Rotation.fromEulerAngles(
        rot=euler * signs, seq=sequence_wanted
    ).to_array()
    if not np.allclose(new_R, extra_R_from_initial_euler_and_factors):
        raise RuntimeError("The rebuilt rotation matrix is not the same as the original one")

    # print("conversion factors to apply to the euler angles are:")
    # print(signs)

    return True, tuple(signs)


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


def get_conversion_from_not_isb_to_isb_oriented_v2(
    parent: BiomechCoordinateSystem,
    child: BiomechCoordinateSystem,
    joint: Joint,
) -> tuple[bool, callable]:
    """
    Get the conversion factor to convert the rotation matrix from the parent segment
    to the child segment to the ISB sequence

    Parameters
    ----------
    parent : BiomechCoordinateSystem
        The parent segment coordinate system
    child : BiomechCoordinateSystem
        The child segment coordinate system
    joint : Joint
        The joint type

    Returns
    -------
    tuple(bool, callable)
        bool
            True if the biomechanical coordinate system is compatible with ISB
        tuple
            The conversion factor for dof1, dof2, dof3 of euler angles

    """
    if joint.joint_type in (JointType.STERNO_CLAVICULAR, JointType.ACROMIO_CLAVICULAR, JointType.SCAPULO_THORACIC):
        sequence_wanted = EulerSequence.YXZ
        # check that we have three different letters in the sequence
        if len(set(joint.euler_sequence.value)) != 3:
            raise RuntimeError(
                "The euler sequence of the joint must have three different letters to be able to convert with factors 1"
                f"or -1 to the ISB sequence {sequence_wanted.value}, but the sequence of the joint is"
                f" {joint.euler_sequence.value}"
            )
    elif joint.joint_type in (JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL):
        sequence_wanted = EulerSequence.YXY
        # check that the sequence in joint.euler_sequence as the same two letters for the first and third rotations
        if joint.euler_sequence.value[0] != joint.euler_sequence.value[2]:
            raise RuntimeError(
                "The euler sequence of the joint must have the same two letters for the first and third rotations"
                f"to be able to convert with factors 1 or -1 to the ISB sequence {sequence_wanted.value},"
                f" but the sequence of the joint is {joint.euler_sequence.value}"
            )
    else:
        raise RuntimeError(
            "The joint type must be JointType.STERNO_CLAVICULAR, JointType.ACROMIO_CLAVICULAR,"
            "JointType.SCAPULO_THORACIC, JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL"
        )

    the_tuple = convert_rotation_matrix_from_one_coordinate_system_to_another(
        parent,  # sending only the parent segment since the two segments have the same orientation
        joint.euler_sequence,
        sequence_wanted,
    )

    return True, the_tuple


#
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
    if segment == Segment.THORAX:
        return ["thorax_x", "thorax_y", "thorax_z", "thorax_origin"]
    elif segment == Segment.CLAVICLE:
        return ["clavicle_x", "clavicle_y", "clavicle_z", "clavicle_origin"]
    elif segment == Segment.SCAPULA:
        return ["scapula_x", "scapula_y", "scapula_z", "scapula_origin"]
    elif segment == Segment.HUMERUS:
        return ["humerus_x", "humerus_y", "humerus_z", "humerus_origin"]
    else:
        raise ValueError(f"{segment} is not a valid segment.")


def get_is_isb_column(segment: Segment) -> str:
    if segment == Segment.THORAX:
        return "thorax_is_isb"
    elif segment == Segment.CLAVICLE:
        return "clavicle_is_isb"
    elif segment == Segment.SCAPULA:
        return "scapula_is_isb"
    elif segment == Segment.HUMERUS:
        return "humerus_is_isb"
    else:
        raise ValueError(f"{segment} is not a valid segment.")


def get_correction_column(segment: Segment) -> str:
    if segment == Segment.THORAX:
        return "thorax_correction_method"
    elif segment == Segment.CLAVICLE:
        return "clavicle_correction_method"
    elif segment == Segment.SCAPULA:
        return "scapula_correction_method"
    elif segment == Segment.HUMERUS:
        return "humerus_correction_method"
    else:
        raise ValueError(f"{segment} is not a valid segment.")


def get_is_correctable_column(segment: Segment) -> str:
    if segment == Segment.THORAX:
        return "thorax_is_isb_correctable"
    elif segment == Segment.CLAVICLE:
        return "clavicle_is_isb_correctable"
    elif segment == Segment.SCAPULA:
        return "scapula_is_isb_correctable"
    elif segment == Segment.HUMERUS:
        return "humerus_is_isb_correctable"
    else:
        raise ValueError(f"{segment} is not a valid segment.")
