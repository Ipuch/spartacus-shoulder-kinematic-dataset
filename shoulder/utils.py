from .enums import CartesianAxis, EulerSequence, JointType, BiomechDirection, BiomechOrigin, Segment
from .angle_conversion_callbacks import get_angle_conversion_callback_from_tuple, get_angle_conversion_callback_from_sequence
import math


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
            if biomech_direction_sign(axis) == 1:
                if axis == BiomechDirection.PlusAnteroPosterior:
                    my_arg["antero_posterior_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusMedioLateral:
                    my_arg["medio_lateral_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusInferoSuperior:
                    my_arg["infero_superior_axis"] = positive_enum
                    continue
            elif biomech_direction_sign(axis) == -1:
                if axis == BiomechDirection.MinusAnteroPosterior:
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

    def is_isb(self) -> bool:
        return self.is_isb_oriented() and self.is_isb_origin()

    def is_isb_oriented(self) -> bool:
        condition_1 = self.anterior_posterior_axis is CartesianAxis.plusX
        condition_2 = self.infero_superior_axis is CartesianAxis.plusY
        condition_3 = self.medio_lateral_axis is CartesianAxis.plusZ
        return condition_1 and condition_2 and condition_3

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
    ):
        self.joint_type = joint_type
        self.euler_sequence = euler_sequence

    def is_joint_sequence_isb(self) -> bool:
        return get_isb_sequence_from_joint_type(self.joint_type) == self.euler_sequence


def check_coordinates_and_euler_sequence_compatibility(
    parent_segment: BiomechCoordinateSystem,
    child_segment: BiomechCoordinateSystem,
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
        # rotation 90° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusY
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=z, x=x, z=-y")
            return True, (1, 1, -1)

        # rotation 180° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-y, x=x, z=-z")
            return True, (-1, 1, -1)

        # rotation 270° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusZ
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusY
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusZ
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-z, x=x, z=y")
            return True, (-1, 1, 1)

        # Rotation -90° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusZ
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusX
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusZ
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusX
        condition[6] = joint.euler_sequence == EulerSequence.YZX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=-z, z=x")
            return True, (1, -1, 1)

        # Rotation 180° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=-x, z=-z")
            return True, (1, -1, -1)

        # Rotation -270° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusZ
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusX
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusZ
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusX
        condition[6] = joint.euler_sequence == EulerSequence.YZX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=y, x=z, z=-x")
            return True, (1, 1, -1)

        # Rotation 90° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusY
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusX
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusY
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusX
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=x, x=-y, z=z")
            return True, (1, -1, 1)

        # Rotation -90° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusY
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusX
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusY
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusX
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-x, x=y, z=z")
            return True, (-1, 1, 1)

        # Rotation 180° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXZ." "y=-y, x=-x, z=z")
            return True, (-1, -1, 1)

        print("This is not a valid combination, of the ISB sequence YXZ.")
        return False, (0, 0, 0)

    # all the joints have the same rotation sequence for the ISB YXY
    elif joint.joint_type in (JointType.GLENO_HUMERAL, JointType.THORACO_HUMERAL):
        # Rotation -90° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusZ
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusY
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusZ
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=z, x=x, y=z")
            return True, (1, 1, 1)

        # Rotation 90° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusZ
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusY
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusZ
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusY
        condition[6] = joint.euler_sequence == EulerSequence.ZXZ

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-z, x=x, y=-z")
            return True, (-1, 1, -1)

        # Rotation 180° along X for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-y, x=x, y=-y")
            return True, (-1, 1, -1)

        # Rotation -90° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusZ
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusX
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusZ
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusX
        condition[6] = joint.euler_sequence == EulerSequence.YZY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=-z, y=y")
            return True, (1, -1, 1)

        # Rotation 90° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusZ
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusX
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusZ
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusX
        condition[6] = joint.euler_sequence == EulerSequence.YZY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=z, y=y")
            return True, (1, 1, 1)

        # Rotation 180° along Y for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.minusZ
        condition[6] = joint.euler_sequence == EulerSequence.YXY

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=y, x=-x, y=y")
            return True, (1, -1, 1)

        # Rotation -90° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.plusY
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusX
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.plusY
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusX
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=-x, x=y, y=-x")
            return True, (-1, 1, -1)

        # Rotation 90° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusY
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.plusX
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusY
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.plusX
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[6] = joint.euler_sequence == EulerSequence.XYX

        if all(condition):
            print("This is a valid combination, of the ISB sequence YXY." " y=x, x=-y, y=x")
            return True, (1, -1, 1)

        # Rotation 180° along Z for each segment coordinate system
        condition[0] = parent_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[1] = parent_segment.infero_superior_axis == CartesianAxis.minusY
        condition[2] = parent_segment.medio_lateral_axis == CartesianAxis.plusZ
        condition[3] = child_segment.anterior_posterior_axis == CartesianAxis.minusX
        condition[4] = child_segment.infero_superior_axis == CartesianAxis.minusY
        condition[5] = child_segment.medio_lateral_axis == CartesianAxis.plusZ
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


def check_biomech_consistency(
    parent_segment: BiomechCoordinateSystem,
    child_segment: BiomechCoordinateSystem,
    joint: Joint,
) -> tuple[bool, callable]:
    """
    Check if the biomechanical coordinate system of the parent and child segment
    are compatible with the joint type and ISB sequences

    Parameters
    ----------
    parent_segment : BiomechCoordinateSystem
        The parent segment coordinate system
    child_segment : BiomechCoordinateSystem
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

    parent_isb = parent_segment.is_isb_oriented()
    child_isb = child_segment.is_isb_oriented()

    if parent_isb and child_isb:
        if joint.is_joint_sequence_isb():
            return True, get_angle_conversion_callback_from_tuple((1, 1, 1))
        else:
            # rebuild the rotation matrix from angles and sequence and identify the ISB angles from the rotation matrix
            return True, get_angle_conversion_callback_from_sequence(previous_sequence=joint.euler_sequence,
                                                                     new_sequence=get_isb_sequence_from_joint_type(
                                                                            joint_type=joint.joint_type
                                                                     )
                                                                     )
    elif not parent_isb or not child_isb:
        output = check_coordinates_and_euler_sequence_compatibility(
            parent_segment=parent_segment,
            child_segment=child_segment,
            joint=joint,
        )
        if output[0]:
            return output[0], get_angle_conversion_callback_from_tuple(output[1])
        else:
            # return print("NotImplementedError: Check conversion not implemented yet")
            return output[0], get_angle_conversion_callback_from_tuple(output[1])
    else:
        raise NotImplementedError("Check conversion not implemented yet")


def biomech_direction_string_to_enum(biomech_direction: str) -> BiomechDirection:
    if biomech_direction == "+mediolateral":
        return BiomechDirection.PlusMedioLateral
    elif biomech_direction == "+anteroposterior":
        return BiomechDirection.PlusAnteroPosterior
    elif biomech_direction == "+inferosuperior":
        return BiomechDirection.PlusInferoSuperior
    elif biomech_direction == "-mediolateral":
        return BiomechDirection.MinusMedioLateral
    elif biomech_direction == "-anteroposterior":
        return BiomechDirection.MinusAnteroPosterior
    elif biomech_direction == "-inferosuperior":
        return BiomechDirection.MinusInferoSuperior
    else:
        raise ValueError(
            f"{biomech_direction} is not a valid biomech_direction."
            "biomech_direction must be one of the following: "
            "+mediolateral, +anteroposterior, +inferosuperior, "
            "-mediolateral, -anteroposterior, -inferosuperior"
        )


def biomech_origin_string_to_enum(biomech_origin: str) -> BiomechOrigin:
    if biomech_origin == "T7":
        return BiomechOrigin.Thorax.T7
    elif biomech_origin == "IJ":
        return BiomechOrigin.Thorax.IJ
    elif biomech_origin == "T1 anterior face":
        return BiomechOrigin.Thorax.T1_ANTERIOR_FACE
    elif biomech_origin == "GH":
        return BiomechOrigin.Humerus.GLENOHUMERAL_HEAD
    elif biomech_origin == "midpoint EM EL":
        return BiomechOrigin.Humerus.MIDPOINT_CONDYLES
    elif biomech_origin == "SC":
        return BiomechOrigin.Clavicle.STERNOCLAVICULAR_JOINT_CENTER
    elif biomech_origin == "volume centroid of a cylinder mapped to the midthird of the clavicle":
        return BiomechOrigin.Clavicle.MIDTHIRD
    elif biomech_origin == "point of intersection between the mesh model and the Zc axis":
        return BiomechOrigin.Clavicle.CUSTOM
    elif biomech_origin == "AC":
        return BiomechOrigin.Scapula.ACROMIOCLAVICULAR_JOINT_CENTER
    elif biomech_origin == "AA":
        return BiomechOrigin.Scapula.ANGULAR_ACROMIALIS
    elif biomech_origin == "glenoid center":
        return BiomechOrigin.Scapula.GLENOID_CENTER
    elif biomech_origin == "TS":
        return BiomechOrigin.Scapula.TRIGNONUM_SPINAE
    elif biomech_origin == "clavicle origin":
        return BiomechOrigin.Clavicle.CUSTOM
    elif biomech_origin == "nan" or biomech_origin == "None" or math.isnan(biomech_origin):
        return None
    else:
        raise ValueError(
            f"{biomech_origin} is not a valid biomech_origin."
            "biomech_origin must be one of the following: "
            "joint, parent, child"
        )


def biomech_direction_sign(direction: BiomechDirection) -> int:
    if direction in (
        BiomechDirection.PlusMedioLateral,
        BiomechDirection.PlusAnteroPosterior,
        BiomechDirection.PlusInferoSuperior,
    ):
        return 1
    elif direction in (
        BiomechDirection.MinusMedioLateral,
        BiomechDirection.MinusAnteroPosterior,
        BiomechDirection.MinusInferoSuperior,
    ):
        return -1
    else:
        raise ValueError(f"{direction} is not a valid BiomechDirection.")


def joint_string_to_enum(joint: str) -> JointType:
    if joint == "glenohumeral":
        return JointType.GLENO_HUMERAL
    elif joint == "acromioclavicular":
        return JointType.ACROMIO_CLAVICULAR
    elif joint == "sternoclavicular":
        return JointType.STERNO_CLAVICULAR
    elif joint == "thoracohumeral":
        return JointType.THORACO_HUMERAL
    elif joint == "scapulothoracic":
        return JointType.SCAPULO_THORACIC
    else:
        raise ValueError(f"{joint} is not a valid joint.")


def euler_sequence_to_enum(sequence: str) -> EulerSequence:
    if sequence == "xyz":
        return EulerSequence.XYZ
    elif sequence == "xzy":
        return EulerSequence.XZY
    elif sequence == "xyx":
        return EulerSequence.XYX
    elif sequence == "xzx":
        return EulerSequence.XZX
    elif sequence == "yzx":
        return EulerSequence.YZX
    elif sequence == "yxz":
        return EulerSequence.YXZ
    elif sequence == "yxy":
        return EulerSequence.YXY
    elif sequence == "yzy":
        return EulerSequence.YZY
    elif sequence == "zxy":
        return EulerSequence.ZXY
    elif sequence == "zyx":
        return EulerSequence.ZYX
    elif sequence == "zxz":
        return EulerSequence.ZXZ
    elif sequence == "zyz":
        return EulerSequence.ZYZ
    else:
        raise ValueError(f"{sequence} is not a valid euler sequence.")


def check_parent_child_joint(joint_type: JointType, parent_name: str, child_name: str) -> bool:
    parent_segment = segment_str_to_enum(parent_name)
    child_segment = segment_str_to_enum(child_name)

    if joint_type == JointType.GLENO_HUMERAL:
        return parent_segment == Segment.SCAPULA and child_segment == Segment.HUMERUS
    elif joint_type == JointType.ACROMIO_CLAVICULAR:
        return parent_segment == Segment.CLAVICLE and child_segment == Segment.SCAPULA
    elif joint_type == JointType.STERNO_CLAVICULAR:
        return parent_segment == Segment.THORAX and child_segment == Segment.CLAVICLE
    elif joint_type == JointType.THORACO_HUMERAL:
        return parent_segment == Segment.THORAX and child_segment == Segment.HUMERUS
    elif joint_type == JointType.SCAPULO_THORACIC:
        return parent_segment == Segment.THORAX and child_segment == Segment.SCAPULA
    else:
        raise ValueError(f"{joint_type} is not a valid joint type.")


def segment_str_to_enum(segment: str) -> Segment:
    if segment == "clavicle":
        return Segment.CLAVICLE
    elif segment == "humerus":
        return Segment.HUMERUS
    elif segment == "scapula":
        return Segment.SCAPULA
    elif segment == "thorax":
        return Segment.THORAX
    else:
        raise ValueError(f"{segment} is not a valid segment.")


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


def get_isb_sequence_from_joint_type(joint_type: JointType):
    if joint_type == JointType.GLENO_HUMERAL:
        return EulerSequence.YXY
    elif joint_type == JointType.SCAPULO_THORACIC:
        return EulerSequence.YXZ
    elif joint_type == JointType.ACROMIO_CLAVICULAR:
        return EulerSequence.YXZ
    elif joint_type == JointType.STERNO_CLAVICULAR:
        return EulerSequence.YXZ
    elif joint_type == JointType.THORACO_HUMERAL:
        return EulerSequence.YXY
    else:
        raise ValueError("JointType not recognized")