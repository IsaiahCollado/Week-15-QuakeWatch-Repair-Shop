# Repair log

Study group: 4  
Members:

Member 1 - Uno Kabiling

Member 2 - Isaiah Collado

Member 3 - Gab Roman

Member 4 - Jeremiah Padilla

Member 5 - John Ballesteros

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `python run.py` stops with `KeyError: 'depth'` in `features_stage()` before the dashboard is written. | `features_stage()` in `quakewatch.py` called `depth_class(t["depth"])`, whereas the integrated DataFrame column is named `depth_km`. | Updated the line in `quakewatch.py` from `t["depth"]` to `t["depth_km"]`. | `test_depth_class_thresholds_member1` in `tests/test_group.py` (alongside `tests/test_features.py`) | Uno Kabiling (Member 1) |
| 2 | Earthquake event times were incorrectly converted to Manila time, potentially producing incorrect local event hours. | `features_stage()` in `quakewatch.py` used `.dt.tz_localize(None).dt.tz_localize("Asia/Manila")`, which removed the original timezone and assigned Manila time instead of converting the existing timezone. | Replaced the timezone conversion with `t["time"].dt.tz_convert("Asia/Manila")` to correctly convert timestamps into Philippine time. | `test_strongest_event_is_at_night_in_manila` and `test_manila_timezone_conversion_member2` | Isaiah Collado (Member 2) |
| 3 | An M 6.0 quake is labelled *Moderate* instead of *Strong*. | `quakewatch.py`, `MAG_BINS` (line 33). The first bin edge was `6.05`, so 6.0 fell in the Moderate bin. | Changed `6.05` to `5.95` in `MAG_BINS`. | `test_mag_class_edges[6.0-Strong]` and `test_strong_or_above_flag` | Carlos Gabriel D. Roman |
| 4 | Earthquakes east of Mindanao were assigned to a distant city in northern Luzon. | `nearest_city()` in `quakewatch.py` passed event longitude before latitude to `haversine_km()`, which expects latitude then longitude. | Passed event latitude first and longitude second; left city coordinate order and vectorized nearest-city calculation unchanged. | `test_mindanao_nearest_city_uses_latitude_longitude_order` and `test_nearest_city_of_known_events` | Jeremiah Daniel Padila (Member 4) |
| 5 | Running the pipeline twice duplicates every quake. | | | | |
| 6 | A row with depth -5 km is not rejected. | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_depth_class_thresholds_member1` | Regular pytest test | Verifies that depth values are classified into shallow, intermediate, and deep categories correctly. | Yes | Uno Kabiling (Member 1) |
| `test_manila_timezone_conversion_member2` | Regular pytest test | Verifies that timestamps are correctly converted to Asia/Manila time while preserving the original moment in time. | Yes | Isaiah Collado (Member 2) |
| `test_strong_or_above_flag` | `parametrize` | Magnitudes below 6.0 are not "Strong or above"; 6.0 and up are. | Yes | Carlos Gabriel D. Roman (Member 3) |
| `test_mindanao_nearest_city_uses_latitude_longitude_order` | `loaded` fixture | Confirms the east-Mindanao event is matched to Butuan after the coordinate-order fix. | Yes | Member 4 |
| | fake API (`responses` or `monkeypatch`) | | | |
| | `caplog` | | | |

## Logging we added

| Where (function) | Level | Message | Why this level |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |

## One thing we learned about debugging

(two or three sentences)