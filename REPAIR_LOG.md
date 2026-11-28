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
| 5 | Running `load_new()` a second time saved duplicate records again (`test_second_load_adds_nothing` failed with `462` new rows instead of `0`, and duplicate IDs appeared). | `load_new()` queried from `FIRST_DAY` and wrote fetched rows to `data/raw` without checking existing raw IDs or filtering duplicates. | Updated `load_new()` in `quakewatch.py` to check `watermark()` / existing IDs in `RAW`, filter out already-saved IDs and duplicate IDs, and only write new rows when non-empty. | `tests/test_acquire.py::test_second_load_adds_nothing`, `tests/test_acquire.py::test_ids_stay_unique_after_two_loads`, `tests/test_group.py::test_load_new_deduplicates_existing_ids`. | John Christian Ballesteros (Member 5) |
| 6 | Rows failing contract rules (such as negative `depth_km = -5`) were not moved to `rejects` and did not emit a `WARNING` log (`test_bad_rows_are_set_aside` failed). | `split_by_contract()` caught validation errors and returned `raw` with an empty `rejects` DataFrame without filtering bad rows or logging a warning. | Updated `split_by_contract()` in `quakewatch.py` to separate valid and invalid rows using boolean checks against contract rules, return `(good, rejects)`, and log a `WARNING` when rows are rejected. | `tests/test_integrate.py::test_bad_rows_are_set_aside`, `tests/test_group.py::test_split_by_contract_rejects_negative_depth_and_logs_warning`, `tests/test_group.py::test_split_by_contract_depth_bounds`. | John Christian Ballesteros (Member 5) |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_depth_class_thresholds_member1` | Regular pytest test | Verifies that depth values are classified into shallow, intermediate, and deep categories correctly. | Yes | Uno Kabiling (Member 1) |
| `test_manila_timezone_conversion_member2` | Regular pytest test | Verifies that timestamps are correctly converted to Asia/Manila time while preserving the original moment in time. | Yes | Isaiah Collado (Member 2) |
| `test_strong_or_above_flag` | `parametrize` | Magnitudes below 6.0 are not "Strong or above"; 6.0 and up are. | Yes | Carlos Gabriel D. Roman (Member 3) |
| `test_mindanao_nearest_city_uses_latitude_longitude_order` | `loaded` fixture | Confirms the east-Mindanao event is matched to Butuan after the coordinate-order fix. | Yes | Member 4 |
| test_split_by_contract_rejects_negative_depth_and_logs_warning | caplog | Negative depth (-5.0) is excluded from good, placed in rejects, and emits a WARNING log. | Yes | John Christian Ballesteros (Member 5) |
| test_load_new_deduplicates_existing_ids | fake API (monkeypatch) | Re-running load_new() skips already-saved IDs and returns 0 new rows on the second call. | Yes | John Christian Ballesteros (Member 5) |
| test_split_by_contract_depth_bounds | parametrize | Boundary depths (-5.0, 0.0, 350.0, 701.0) are accepted or rejected according to contract limits. | Yes | John Christian Ballesteros (Member 5) |

## Logging we added

| Where (function) | Level | Message | Why this level |
| --- | --- | --- | --- |
| split_by_contract | WARNING | Rejected %d row(s) failing data contract | Bad rows are skipped without crashing the pipeline, so a warning flags unexpected/invalid input worth inspecting. |
| | | | |
| | | | |

## One thing we learned about debugging

Testing one change at a time with pytest makes it much easier to separate a real fix from side effects or unrelated errors. Checking actual data types and edge cases - such as why a per-row DataFrame conversion rejected every row - prevents masking one bug with another.
