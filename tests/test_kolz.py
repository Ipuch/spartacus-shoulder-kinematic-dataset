import pytest

from shoulder.kolz_matrices import get_kolz_rotation_matrix
from shoulder.enums import Correction


def test_kolz():
    R = get_kolz_rotation_matrix(Correction.SCAPULA_KOLZ_AC_TO_PA_ROTATION)
    assert R.shape == (3, 3)
    assert R[0, 0] == 0.965
    assert R[0, 1] == -0.057
    assert R[0, 2] == 0.257
    assert R[1, 0] == 0.010
    assert R[1, 1] == 0.984
    assert R[1, 2] == 0.180
    assert R[2, 0] == -0.263
    assert R[2, 1] == 0.171
    assert R[2, 2] == 0.950

    R = get_kolz_rotation_matrix(Correction.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION)
    assert R.shape == (3, 3)
    assert R[0, 0] == 0.949
    assert R[0, 1] == -0.056
    assert R[0, 2] == 0.310
    assert R[1, 0] == 0.010
    assert R[1, 1] == 0.978
    assert R[1, 2] == -0.208
    assert R[2, 0] == -0.314
    assert R[2, 1] == 0.200
    assert R[2, 2] == 0.928

    with pytest.raises(ValueError):
        get_kolz_rotation_matrix(correction=Correction.TO_ISB_ROTATION)
        