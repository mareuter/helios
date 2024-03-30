# Copyright 2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Information models for the application."""

from __future__ import annotations

from pydantic import BaseModel

__all__ = ["DayInformation", "SkyTransitions", "TimerInformation"]


class SkyTransitions(BaseModel):
    """Sky transition information model."""

    astronomical_dawn: float
    nautical_dawn: float
    civil_dawn: float
    sunrise: float
    sunset: float
    civil_dusk: float
    nautical_dusk: float
    astronomical_dusk: float


class DayInformation(SkyTransitions):
    """Day information model."""

    day_length: float


class TimerInformation(BaseModel):
    """Timer information model."""

    date: str
    check_time_utc: int
    sunrise_usno: str
    sunset_usno: str
    on_time_utc: int
    on_time: str
    off_time_utc: int
    off_time: str
