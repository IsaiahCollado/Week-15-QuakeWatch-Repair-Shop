
import pandas as pd
import quakewatch as qw


def test_depth_class_thresholds_member1():
    depths = pd.Series([10, 50, 100, 200, 350])

    result = qw.depth_class(depths)

    expected = ["shallow", "shallow", "intermediate", "intermediate", "deep"]

    assert list(result) == expected


def test_manila_timezone_conversion_member2(loaded):
    qw.integrate()
    feat = qw.features_stage()

    expected = feat["time"].dt.tz_convert("Asia/Manila")

    pd.testing.assert_series_equal(
        feat["local"],
        expected,
        check_names=False
    )
