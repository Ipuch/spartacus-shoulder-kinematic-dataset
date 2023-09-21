from spartacus.src.angle_conversion_callbacks import (
    get_angle_conversion_callback_from_sequence,
    get_angle_conversion_callback_from_tuple,
    EulerSequence,
)
import pytest


def test_checks():
    callack = get_angle_conversion_callback_from_tuple((1, 1, 1))
    assert callack(1, 2, 3) == (1, 2, 3)
    callack = get_angle_conversion_callback_from_tuple((-1, 1, -1))
    assert callack(1, 2, 3) == (-1, 2, -3)
    callack = get_angle_conversion_callback_from_tuple((1, -1, 1))
    assert callack(1, 2, 3) == (1, -2, 3)
    with pytest.raises(ValueError, match="tuple_factors must be a tuple of 1 and -1"):
        get_angle_conversion_callback_from_tuple((1, 1, 2))

    with pytest.raises(ValueError, match="previous_sequence and new_sequence must be different"):
        get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.XYZ)

    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.XZY)
    assert tuple(callack(1, 2, 3)) == (-2.2704912057792535, -0.0587604536838258, 1.1453860614822349)
    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.YXZ)
    assert tuple(callack(1, 2, 3)) == (1.8132071664631333, -0.3577584477324125, -2.3272248511837774)
    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.YZX)
    assert tuple(callack(1, 2, 3)) == (-0.9730597100541793, -0.7494588683753458, -2.6428244606568714)
    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.ZXY)
    assert tuple(callack(1, 2, 3)) == (-3.050495162685674, -0.8690536087868346, -1.926553531745191)
    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.ZYX)
    assert tuple(callack(1, 2, 3)) == (-1.0268907336660056, -0.6499256902050641, -1.857115353462594)
    callack = get_angle_conversion_callback_from_sequence(EulerSequence.XYZ, EulerSequence.YXY)
    assert tuple(callack(1, 2, 3)) == (3.064847992801699, 2.2690392880128885, -2.045600530404556)
