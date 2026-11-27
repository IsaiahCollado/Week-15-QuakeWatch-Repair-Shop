# Repair log

Study group: 4   Members: 
Member 1 - Uno Kabiling
Member 2 - Isaiah Collado
Member 3 - Gab Roman
Member 4 - Jeremiah Padilla
Member 5 - John Ballesteros

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `python run.py` stops with `KeyError: 'depth'` in `features_stage()` before the dashboard is written. | `features_stage()` in `quakewatch.py` (line 177) called `depth_class(t["depth"])`, whereas the integrated DataFrame column is named `depth_km`. | Updated line 177 in `quakewatch.py` from `t["depth"]` to `t["depth_km"]`. | `test_depth_class_thresholds_member1` in `tests/test_group.py` (alongside `tests/test_features.py`) | Uno Kabiling (Member 1) |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

## Logging we added

| Where (function) | Level | Message | Why this level |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |

## One thing we learned about debugging

(two or three sentences)
