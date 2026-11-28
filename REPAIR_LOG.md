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
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_depth_class_thresholds_member1` | Regular pytest test | Verifies that depth values are classified into shallow, intermediate, and deep categories correctly. | Yes | Uno Kabiling (Member 1) |
| `test_manila_timezone_conversion_member2` | Regular pytest test | Verifies that timestamps are correctly converted to Asia/Manila time while preserving the original moment in time. | Yes | Isaiah Collado (Member 2) |
| | | | | |
