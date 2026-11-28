# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | Running `load_new()` a second time saved duplicate records again (`test_second_load_adds_nothing` failed with `462` new rows instead of `0`, and duplicate IDs appeared). | `load_new()` queried from `FIRST_DAY` and wrote fetched rows to `data/raw` without checking existing raw IDs or filtering duplicates. | Updated `load_new()` in `quakewatch.py` to check `watermark()` / existing IDs in `RAW`, filter out already-saved IDs and duplicate IDs, and only write new rows when non-empty. | `tests/test_acquire.py::test_second_load_adds_nothing`, `tests/test_acquire.py::test_ids_stay_unique_after_two_loads`, `tests/test_group.py::test_load_new_deduplicates_existing_ids`. | John Christian Ballesteros (Member 5) |
| 6 | Rows failing contract rules (such as negative `depth_km = -5`) were not moved to `rejects` and did not emit a `WARNING` log (`test_bad_rows_are_set_aside` failed). | `split_by_contract()` caught validation errors and returned `raw` with an empty `rejects` DataFrame without filtering bad rows or logging a warning. | Updated `split_by_contract()` in `quakewatch.py` to separate valid and invalid rows using boolean checks against contract rules, return `(good, rejects)`, and log a `WARNING` when rows are rejected. | `tests/test_integrate.py::test_bad_rows_are_set_aside`, `tests/test_group.py::test_split_by_contract_rejects_negative_depth_and_logs_warning`, `tests/test_group.py::test_split_by_contract_depth_bounds`. | John Christian Ballesteros (Member 5) |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
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
