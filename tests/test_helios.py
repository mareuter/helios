# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from datetime import datetime

from app.helios import Helios


def test_internal_parameters() -> None:
    h = Helios()
    assert h.ephemeris is not None
    assert h.timescale is not None


def test_sky_transitions() -> None:
    h = Helios()
    current_datetime = datetime(2023, 3, 3, 14, 56, 0)
    timezone = "US/Eastern"
    latitude = 40.8939
    longitude = -83.8917

    sky_transitions = h.sky_transitions(latitude, longitude, current_datetime, timezone)
    assert len(list(sky_transitions.keys())) == 8
    assert sky_transitions["Astronomical Dawn"].timestamp() == 1677839749.146742
    assert sky_transitions["Nautical Dawn"].timestamp() == 1677841657.360251
    assert sky_transitions["Civil Dawn"].timestamp() == 1677843561.421941
    assert sky_transitions["Sunrise"].timestamp() == 1677845209.722515
    assert sky_transitions["Sunset"].timestamp() == 1677886123.971968
    assert sky_transitions["Civil Dusk"].timestamp() == 1677887774.573878
    assert sky_transitions["Nautical Dusk"].timestamp() == 1677889681.943577
    assert sky_transitions["Astronomical Dusk"].timestamp() == 1677891594.401842
