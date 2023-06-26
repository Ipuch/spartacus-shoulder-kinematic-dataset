from .enums import CartesianAxis, EulerSequence, JointType, BiomechDirection


class BiomechCoordinateSystem:
    def __init__(
        self,
        antero_posterior_axis: CartesianAxis,
        infero_superior_axis: CartesianAxis,
        medio_lateral_axis: CartesianAxis,
        origin=None,
    ):
        self.anterior_posterior_axis = antero_posterior_axis
        self.infero_superior_axis = infero_superior_axis
        self.medio_lateral_axis = medio_lateral_axis
        self.origin = origin

    @classmethod
    def from_biomech_directions(
        cls,
        x: BiomechDirection,
        y: BiomechDirection,
        z: BiomechDirection,
        origin=None,
    ):
        my_arg = dict()
        my_arg["origin"] = origin

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
                    my_arg["antero_posterior_axis"] = negative_enums_axis
                    continue
                elif axis == BiomechDirection.MinusMedioLateral:
                    my_arg["medio_lateral_axis"] = negative_enums_axis
                    continue
                elif axis == BiomechDirection.MinusInferoSuperior:
                    my_arg["infero_superior_axis"] = negative_enums_axis
                    continue

        return cls(*my_arg)

    def is_isb(self) -> bool:
        condition_1 = self.anterior_posterior_axis is CartesianAxis.plusX
        condition_2 = self.infero_superior_axis is CartesianAxis.plusY
        condition_3 = self.medio_lateral_axis is CartesianAxis.plusZ
        return condition_1 and condition_2 and condition_3


class Joint:
    def __init__(
        self,
        joint_type: JointType,
        euler_sequence: EulerSequence,
    ):
        self.joint_type = joint_type
        self.euler_sequence = euler_sequence

    def is_joint_sequence_isb(self) -> bool:
        if self.joint_type == JointType.GLENO_HUMERAL:
            return self.euler_sequence is EulerSequence.YXY
        elif self.joint_type == JointType.SCAPULO_THORACIC:
            return self.euler_sequence is EulerSequence.YXZ
        elif self.joint_type == JointType.ACROMIO_CLAVICULAR:
            return self.euler_sequence is EulerSequence.YXZ
        elif self.joint_type == JointType.STERNO_CLAVICULAR:
            return self.euler_sequence is EulerSequence.YXZ
        elif self.joint_type == JointType.THORACO_HUMERAL:
            return self.euler_sequence is EulerSequence.YXY
        else:
            raise ValueError("JointType not recognized")


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
    if joint.joint_type.STERNO_CLAVICULAR or joint.joint_type.ACROMIO_CLAVICULAR or joint.joint_type.SCAPULO_THORACIC:
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
) -> tuple[bool, tuple[int, int, int]]:
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
    tuple(bool, tuple(int, int, int))
        bool
            True if the biomechanical coordinate system is compatible with ISB
        tuple
            The conversion factor for dof1, dof2, dof3 of euler angles


    """

    parent_isb = parent_segment.is_isb()
    child_isb = child_segment.is_isb()

    if parent_isb and child_isb:
        if joint.is_joint_sequence_isb():
            return True, (1, 1, 1)
        else:
            raise NotImplementedError("Check conversion not implemented yet")
    elif not parent_isb or not child_isb:
        output = check_coordinates_and_euler_sequence_compatibility(
            parent_segment=parent_segment,
            child_segment=child_segment,
            joint=joint,
        )
        if output[0]:
            return output
        else:
            return print("NotImplementedError: Check conversion not implemented yet")
            # raise NotImplementedError("Check conversion not implemented yet")
    else:
        raise NotImplementedError("Check conversion not implemented yet")


def biomech_direction_string_to_enum(biomech_direction: str) -> BiomechDirection:
    if biomech_direction == "+mediolateral":
        return BiomechDirection.PlusMedioLateral
    elif biomech_direction == "+anteroposterior":
        return BiomechDirection.PlusAnteroPosterior
    elif biomech_direction == "+superoinferior":
        return BiomechDirection.PlusInferoSuperior
    elif biomech_direction == "-mediolateral":
        return BiomechDirection.MinusMedioLateral
    elif biomech_direction == "-anteroposterior":
        return BiomechDirection.MinusAnteroPosterior
    elif biomech_direction == "-superoinferior":
        return BiomechDirection.MinusInferoSuperior
    else:
        raise ValueError(
            f"{biomech_direction} is not a valid biomech_direction."
            "biomech_direction must be one of the following: "
            "+mediolateral, +anteroposterior, +inferosuperior, "
            "-mediolateral, -anteroposterior, -inferosuperior"
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
