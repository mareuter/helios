# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for formatters."""

from __future__ import annotations

import datetime
import zoneinfo

from helios.formatters import date_format, day_length_format, time_format


def test_date_format() -> None:
    localtime = datetime.datetime(2023, 3, 3, 14, 56, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern"))
    date_string = date_format(localtime)
    assert date_string == "March 3, 2023"


def test_time_format() -> None:
    localtime = datetime.datetime(2023, 3, 3, 14, 56, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern"))
    time_string = time_format(localtime)
    assert time_string == "14:56"
    localtime += datetime.timedelta(seconds=30)
    time_string = time_format(localtime)
    assert time_string == "14:57"


def test_day_length_format() -> None:
    day_length = datetime.timedelta(seconds=44526)
    day_length_string = day_length_format(day_length)
    assert day_length_string == "12 hours, 22 minutes and 6 seconds"
