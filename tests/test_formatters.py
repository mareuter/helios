# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import datetime

import pytz

from app.formatters import date_format, time_format


def test_date_format() -> None:
    localtime = datetime.datetime(
        2023, 3, 3, 14, 56, 0, tzinfo=pytz.timezone("US/Eastern")
    )
    date_string = date_format(localtime)
    assert "March 3, 2023" == date_string


def test_time_format() -> None:
    localtime = datetime.datetime(
        2023, 3, 3, 14, 56, 0, tzinfo=pytz.timezone("US/Eastern")
    )
    time_string = time_format(localtime)
    assert "14:56" == time_string
    localtime += datetime.timedelta(seconds=30)
    time_string = time_format(localtime)
    assert "14:57" == time_string
