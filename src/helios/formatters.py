# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Module containing formatting support."""

from __future__ import annotations

from datetime import datetime, timedelta


def date_format(date: datetime) -> str:
    """Format date to Month Name Day, Year.

    Parameters
    ----------
    date : datetime
        The current date/time to format.

    Returns
    -------
    str
        The formatted date string.
    """
    return date.strftime("%B %-d, %Y")


def day_length_format(length: timedelta) -> str:
    """Format length of day into hours, minutes and seconds.

    Parameters
    ----------
    length : timedelta
        The calculated length of day.

    Returns
    -------
    str
        The formatted day length string.
    """
    hours = int(length.seconds / 3600)
    minutes = int(length.seconds % 3600 / 60)
    seconds = int(length.seconds % 3600 % 60)
    return f"{hours} hours, {minutes} minutes and {seconds} seconds"


def time_format(time: datetime) -> str:
    """Format time to Hours(24):Minutes(zero padded).

    Times are rounded to nearest minute to agree with the US Naval Observatory.

    Parameters
    ----------
    time : datetime
        The current time to format.

    Returns
    -------
    str
        The formatted time string
    """
    time += timedelta(seconds=30)
    return time.strftime("%H:%M")
