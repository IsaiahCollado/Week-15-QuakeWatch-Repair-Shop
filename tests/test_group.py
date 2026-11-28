"""Our group's own tests for QuakeWatch (DSA 4153, Week 15)."""

import logging
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


def test_mindanao_nearest_city_uses_latitude_longitude_order(loaded):
    clean = qw.integrate()
    event = clean[clean["time"].dt.strftime("%Y-%m-%d %H:%M") == "2023-12-02 14:37"]

    assert event["city_id"].iloc[0] == "C10"


def test_split_by_contract_rejects_negative_depth_and_logs_warning(caplog):
    raw = pd.DataFrame([
        {
            "id": "good-1",
            "time": pd.Timestamp("2024-01-01T00:00:00Z"),
            "latitude": 14.5,
            "longitude": 121.0,
            "depth_km": 10.0,
            "mag": 5.5,
            "magType": "mww",
            "place": "Manila",
        },
        {
            "id": "bad-neg-depth",
            "time": pd.Timestamp("2024-01-01T01:00:00Z"),
            "latitude": 14.5,
            "longitude": 121.0,
            "depth_km": -5.0,
            "mag": 5.5,
            "magType": "mww",
            "place": "Manila",
        },
    ])

    with caplog.at_level(logging.WARNING, logger="quakewatch"):
        good, rejects = qw.split_by_contract(raw)

    assert "bad-neg-depth" not in set(good["id"])
    assert "bad-neg-depth" in set(rejects["id"])
    assert any(r.levelno == logging.WARNING for r in caplog.records)


# 2. monkeypatch test (guards Defect 5: load_new skips already-saved IDs)
def test_load_new_deduplicates_existing_ids(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    monkeypatch.setattr(qw, "RAW", raw_dir)

    sample = pd.DataFrame([
        {
            "id": "eq-1",
            "time": pd.Timestamp("2024-02-01T00:00:00Z"),
            "latitude": 10.0,
            "longitude": 125.0,
            "depth_km": 20.0,
            "mag": 5.4,
            "magType": "mww",
            "place": "Leyte",
        }
    ])

    monkeypatch.setattr(qw, "fetch_range", lambda start, end, limit=100, session=None: sample.copy())

    first_count = qw.load_new("2024-03-01")
    second_count = qw.load_new("2024-03-01")

    assert first_count == 1
    assert second_count == 0


# 3. parametrize test (guards Defect 6 boundary checks on depth_km)
@pytest.mark.parametrize("depth,expected_valid", [
    (-5.0, False),
    (0.0, True),
    (350.0, True),
    (701.0, False),
])
def test_split_by_contract_depth_bounds(depth, expected_valid):
    raw = pd.DataFrame([
        {
            "id": f"eq-{depth}",
            "time": pd.Timestamp("2024-03-01T00:00:00Z"),
            "latitude": 14.0,
            "longitude": 121.0,
            "depth_km": depth,
            "mag": 5.2,
            "magType": "mww",
            "place": "Luzon",
        }
    ])
    good, rejects = qw.split_by_contract(raw)
    assert (len(good) == 1) is expected_valid
    assert (len(rejects) == 0) is expected_valid
