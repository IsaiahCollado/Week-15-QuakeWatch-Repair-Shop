"""Our group's own tests for QuakeWatch (DSA 4153, Week 15)."""

import pandas as pd
import pytest
import quakewatch as qw


# ---------------------------------------------------------------------------
# Member 1 - Uno Kabiling
# Tests depth classification.
# ---------------------------------------------------------------------------
def test_depth_class_thresholds_member1():
    depths = pd.Series([10, 50, 100, 200, 350])

    result = qw.depth_class(depths)

    expected = ["shallow", "shallow", "intermediate", "intermediate", "deep"]

    assert list(result) == expected


# ---------------------------------------------------------------------------
# Member 2 - Isaiah Collado
# Tests Manila timezone conversion.
# ---------------------------------------------------------------------------
def test_manila_timezone_conversion_member2(loaded):
    qw.integrate()
    feat = qw.features_stage()

    expected = feat["time"].dt.tz_convert("Asia/Manila")

    pd.testing.assert_series_equal(
        feat["local"],
        expected,
        check_names=False
    )


# ---------------------------------------------------------------------------
# Member 3 - Carlos Gabriel D. Roman
# Guards Defect 3 using parameterized tests.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("mag, strong_or_above", [
    (5.0, False),
    (5.9, False),
    (6.0, True),
    (6.1, True),
    (6.9, True),
    (7.0, True),
    (8.0, True),
])
def test_strong_or_above_flag(mag, strong_or_above):
    label = qw.mag_class(pd.Series([mag]))

    assert bool((label >= "Strong").iloc[0]) is strong_or_above