import numpy as np
import pytest

from shoulder.kolz_matrices import get_kolz_rotation_matrix
from shoulder.enums import Correction


def test_kolz():
    R = get_kolz_rotation_matrix(Correction.SCAPULA_KOLZ_AC_TO_PA_ROTATION, orthonormalize=False)
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

    R = get_kolz_rotation_matrix(Correction.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION, orthonormalize=False)
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

    R = get_kolz_rotation_matrix(Correction.SCAPULA_KOLZ_AC_TO_PA_ROTATION, orthonormalize=True)
    assert R.shape == (3, 3)
    np.testing.assert_almost_equal(R[0, 0], 9.62130083e-01)
    np.testing.assert_almost_equal(R[0, 1], -5.77424614e-02)
    np.testing.assert_almost_equal(R[0, 2], 2.66404789e-01)
    np.testing.assert_almost_equal(R[1, 0], 5.56368185e-02)
    np.testing.assert_almost_equal(R[1, 1], 9.98331511e-01)
    np.testing.assert_almost_equal(R[1, 2], 1.54511560e-02)
    np.testing.assert_almost_equal(R[2, 0], -2.66852483e-01)
    np.testing.assert_almost_equal(R[2, 1], -4.41071341e-05)
    np.testing.assert_almost_equal(R[2, 2], 9.63737387e-01)
    np.testing.assert_almost_equal(np.linalg.det(R), 1.0)

    with pytest.raises(ValueError):
        get_kolz_rotation_matrix(correction=Correction.TO_ISB_ROTATION)
