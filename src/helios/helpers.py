# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Module for package helpers."""

from __future__ import annotations

from datetime import datetime, timedelta
import random

__all__ = ["get_time_variation"]


def get_time_variation(span: str) -> timedelta:
    """Get a random chuck of time to add to a time.

    Parameters
    ----------
    span : str
        The format in HH:MM:SS for the time range.

    Returns
    -------
    timedelta
        The chuck of time to be added to a time.
    """
    span_time = datetime.strptime(span, "%H:%M:%S").time()
    time_range = timedelta(seconds=span_time.second, minutes=span_time.minute, hours=span_time.hour)
    value = random.randrange(-time_range.seconds, time_range.seconds)
    return timedelta(seconds=value)
