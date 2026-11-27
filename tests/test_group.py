"""Our group's own tests for QuakeWatch (DSA 4153, Week 15).

Each test was run on the broken code (it must FAIL there) and on the repaired code (it must PASS).
Each member adds their tests in their own section below.
"""
import pandas as pd
import pytest

import quakewatch as qw


# ---------------------------------------------------------------------------
# Member 3 - Carlos Gabriel D. Roman
# Guards Defect 3 (Incident 3): an M 6.0 earthquake was labelled "Moderate".
# Tool: @pytest.mark.parametrize
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("mag, strong_or_above", [
    (5.0, False),    # lowest Moderate
    (5.9, False),    # highest Moderate: must stay below "Strong"
    (6.0, True),     # the reported event: USGS says 6.0 is Strong
    (6.1, True),     # broken bin edge was 6.05; check just past the real boundary too
    (6.9, True),
    (7.0, True),
    (8.0, True),
])
def test_strong_or_above_flag(mag, strong_or_above):
    """features_stage() and run_pipeline() count 'Strong or above' with  mag_class >= "Strong".
    This checks that comparison directly, so a wrong bin edge changes the dashboard count."""
    label = qw.mag_class(pd.Series([mag]))
    assert bool((label >= "Strong").iloc[0]) is strong_or_above
