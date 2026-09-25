import numpy as np

import pandas as pd


def test_none_equality() -> None:
    s = pd.Series([1, None, "a", np.nan])

    # == should return True for the None position (index 1)
    res_eq = s == s
    assert res_eq[0]
    assert res_eq[1]
    assert res_eq[2]
    assert not res_eq[3]  # np.nan == np.nan is False

    # != should return False for the None position
    res_ne = s != s
    assert not res_ne[0]
    assert not res_ne[1]
    assert not res_ne[2]
    assert res_ne[3]  # np.nan != np.nan is True

    # < should return False for the None position
    res_lt = s < s
    assert not res_lt[0]
    assert not res_lt[1]
    assert not res_lt[2]
    assert not res_lt[3]

    # Comparing with scalar None
    res_scalar_eq = s == None  # noqa: E711
    assert not res_scalar_eq[0]
    assert res_scalar_eq[1]
    assert not res_scalar_eq[2]
    assert not res_scalar_eq[3]

    res_scalar_ne = s != None  # noqa: E711
    assert res_scalar_ne[0]
    assert not res_scalar_ne[1]
    assert res_scalar_ne[2]
    assert res_scalar_ne[3]

    res_scalar_lt = s < None
    assert not res_scalar_lt[0]
    assert not res_scalar_lt[1]
    assert not res_scalar_lt[2]
    assert not res_scalar_lt[3]
