# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | Earthquakes east of Mindanao were assigned to a distant city in northern Luzon. | `nearest_city()` in `quakewatch.py` passed event longitude before latitude to `haversine_km()`, which expects latitude then longitude. | Passed event latitude first and longitude second; left city coordinate order and vectorized nearest-city calculation unchanged. | `test_mindanao_nearest_city_uses_latitude_longitude_order` and `test_nearest_city_of_known_events` | Member 4 |
| 5 | | | | | |
| 6 | | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| `test_mindanao_nearest_city_uses_latitude_longitude_order` | `loaded` fixture | Confirms the east-Mindanao event is matched to Butuan after the coordinate-order fix. | Yes | Member 4 |
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
