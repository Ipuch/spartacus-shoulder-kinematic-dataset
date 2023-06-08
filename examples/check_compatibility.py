from shoulder import (
    EulerSequence,
    BiomechCoordinateSystem,
    CartesianAxis,
    Joint,
    JointType,
    check_biomech_consistency,
)


def main():
    # A very standard example of the sterno-clavicular joint, already in ISB
    print(" -- Sterno-clavicular joint -- ISB")
    thorax = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.plusX,
        infero_superior_axis=CartesianAxis.plusY,
        medio_lateral_axis=CartesianAxis.plusZ,
    )
    print(thorax.is_isb_oriented())
    clavicle = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.plusX,
        infero_superior_axis=CartesianAxis.plusY,
        medio_lateral_axis=CartesianAxis.plusZ,
    )
    print(clavicle.is_isb_oriented())
    sterno_clav = Joint(
        joint_type=JointType.ACROMIO_CLAVICULAR,
        euler_sequence=EulerSequence.YXZ,
    )
    print(sterno_clav.is_joint_sequence_isb())

    output = check_biomech_consistency(
        parent_segment=thorax,
        child_segment=clavicle,
        joint=sterno_clav,
    )
    print(output)

    # A not standard example of the sterno-clavicular joint, not in ISB
    print(" -- Sterno-clavicular joint -- not ISB")
    thorax = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.plusX,
        infero_superior_axis=CartesianAxis.plusY,
        medio_lateral_axis=CartesianAxis.plusZ,
    )
    print(thorax.is_isb_oriented())
    clavicle = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.minusY,
        infero_superior_axis=CartesianAxis.plusX,
        medio_lateral_axis=CartesianAxis.plusZ,
    )
    print(clavicle.is_isb_oriented())
    sterno_clav = Joint(
        joint_type=JointType.STERNO_CLAVICULAR,
        euler_sequence=EulerSequence.YXZ,
    )
    print(sterno_clav.is_joint_sequence_isb())

    output = check_biomech_consistency(
        parent_segment=thorax,
        child_segment=clavicle,
        joint=sterno_clav,
    )
    print(output)

    # A not standard example of the sterno-clavicular joint, not in ISB, but compatible with ISB
    print(" -- Sterno-clavicular joint -- not ISB but compatible")
    thorax = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.plusX,
        infero_superior_axis=CartesianAxis.plusZ,
        medio_lateral_axis=CartesianAxis.minusY,
    )
    print(thorax.is_isb_oriented())
    clavicle = BiomechCoordinateSystem(
        antero_posterior_axis=CartesianAxis.plusX,
        infero_superior_axis=CartesianAxis.plusZ,
        medio_lateral_axis=CartesianAxis.minusY,
    )
    print(clavicle.is_isb_oriented())
    sterno_clav = Joint(
        joint_type=JointType.STERNO_CLAVICULAR,
        euler_sequence=EulerSequence.ZXY,
    )
    print(sterno_clav.is_joint_sequence_isb())

    output = check_biomech_consistency(
        parent_segment=thorax,
        child_segment=clavicle,
        joint=sterno_clav,
    )
    print(output)


if __name__ == "__main__":
    main()
