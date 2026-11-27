# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `run.py` stops with a `KeyError`. | | | | |
| 2 | Strongest quake shown at 14:37 instead of 22:37 Manila time. | | | | |
| 3 | An M 6.0 quake is labelled *Moderate* instead of *Strong*. | `quakewatch.py`, `MAG_BINS` (line 33). The first bin edge was `6.05`, so 6.0 fell in the Moderate bin. | Changed `6.05` to `5.95` in `MAG_BINS`. | `test_mag_class_edges[6.0-Strong]` | Carlos Gabriel D. Roman |
| 4 | Quakes east of Mindanao are matched to a city in northern Luzon. | | | | |
| 5 | Running the pipeline twice duplicates every quake. | | | | |
| 6 | A row with depth -5 km is not rejected. | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_strong_or_above_flag` | `parametrize` | Magnitudes below 6.0 are not "Strong or above"; 6.0 and up are. | Yes | Carlos Gabriel D. Roman |
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
