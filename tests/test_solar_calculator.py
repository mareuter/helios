# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for solar calculator class."""

from __future__ import annotations

import datetime
from unittest.mock import patch
import zoneinfo

from helios.exceptions import BadTimezone
from helios.solar_calculator import SolarCalculator
import pytest


def test_internal_parameters() -> None:
    h = SolarCalculator()
    assert h.ephemeris is not None
    assert h.timescale is not None


def test_sky_transitions() -> None:
    h = SolarCalculator()
    current_datetime = datetime.datetime(2023, 3, 3, 14, 56, 0).timestamp()
    timezone = "US/Eastern"
    latitude = 40.8939
    longitude = -83.8917

    sky_transitions = h.sky_transitions(latitude, longitude, current_datetime, timezone)
    assert len(list(sky_transitions.keys())) == 8
    assert sky_transitions["Astronomical Dawn"].timestamp() == pytest.approx(1677839749.146742, rel=1e-1)
    assert sky_transitions["Nautical Dawn"].timestamp() == pytest.approx(1677841657.360251, rel=1e-1)
    assert sky_transitions["Civil Dawn"].timestamp() == pytest.approx(1677843561.421941, rel=1e-1)
    assert sky_transitions["Sunrise"].timestamp() == pytest.approx(1677845209.722515, rel=1e-1)
    assert sky_transitions["Sunset"].timestamp() == pytest.approx(1677886123.971968, rel=1e-1)
    assert sky_transitions["Civil Dusk"].timestamp() == pytest.approx(1677887774.573878, rel=1e-1)
    assert sky_transitions["Nautical Dusk"].timestamp() == pytest.approx(1677889681.943577, rel=1e-1)
    assert sky_transitions["Astronomical Dusk"].timestamp() == pytest.approx(1677891594.401842, rel=1e-1)


def test_bad_timezone() -> None:
    h = SolarCalculator()
    current_datetime = datetime.datetime(2023, 3, 3, 14, 56, 0).timestamp()
    timezone = "USA/Santiago"
    latitude = 40.8939
    longitude = -83.8917

    with pytest.raises(BadTimezone):
        h.sky_transitions(latitude, longitude, current_datetime, timezone)


def test_get_localtime() -> None:
    utc = datetime.datetime(2023, 3, 3, 19, 56, 0, tzinfo=datetime.UTC)
    with patch("helios.solar_calculator.SolarCalculator.get_utc", return_value=utc):
        timezone = "US/Eastern"
        localtime = utc.astimezone(zoneinfo.ZoneInfo(timezone))
        assert SolarCalculator.get_localtime(timezone) == localtime
