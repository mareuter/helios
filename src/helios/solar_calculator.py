# Copyright 2023-2025 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Module for calculating sun information."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from importlib.resources import files
import zoneinfo

from skyfield import almanac
from skyfield.api import load, load_file, wgs84

from .exceptions import BadTimezone

__all__ = ["SolarCalculator"]

DATA_PATH = files("helios.data.skyfield").joinpath("de421.bsp")


class SolarCalculator:
    """Class for calculating solar information."""

    def __init__(self) -> None:
        self.timescale = load.timescale()
        self.ephemeris = load_file(DATA_PATH)

    @classmethod
    def get_utc(cls) -> datetime:
        """Get the current UTC time.

        Returns
        -------
        datetime
            The current UTC datetime instance.
        """
        return datetime.now(UTC)

    @classmethod
    def get_localtime(cls, tz_name: str, timestamp: float | None = None) -> datetime:
        """Get the current local time as given by the timezone.

        Parameters
        ----------
        tz_name : str
            The timezone for finding the local time.
        timestamp : float
            An alternate UTC UNIX timestamp.

        Returns
        -------
        datetime
            The current local time instance.
        """
        utcnow = cls.get_utc() if timestamp is None else datetime.fromtimestamp(timestamp)
        zone = zoneinfo.ZoneInfo(tz_name)
        return utcnow.astimezone(zone)

    def sky_transitions(
        self,
        latitude: float,
        longitude: float,
        current_datetime: float,
        location_timezone: str,
    ) -> dict[str, datetime]:
        """Calculate sky transitions.

        This function calculates the eight sky transitions from astronomical
        dawn to astonomical dusk.

        Parameters
        ----------
        latitude : float
            The latitude (decimal degrees) of the location. Negative is South,
            Positive is North.
        longitude : float
            The longitude (decimal degrees) of the location. Negative is West,
            Positive is East.
        current_datetime : float
            The current date and time as a UNIX timestamp in UTC to calculate
            the sky transitions for. Only date is used.
        location_timezone : str
            The timezone for the location.

        Returns
        -------
        dict
            The object containing the name of the sky transition as the key
            and the sky transition date/time.
        """
        try:
            zone = zoneinfo.ZoneInfo(location_timezone)
        except zoneinfo.ZoneInfoNotFoundError:
            raise BadTimezone from None
        now = datetime.fromtimestamp(current_datetime).astimezone(zone)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)

        t0 = self.timescale.from_datetime(midnight)
        t1 = self.timescale.from_datetime(next_midnight)

        location = wgs84.latlon(latitude, longitude)
        f = almanac.dark_twilight_day(self.ephemeris, location)
        times, events = almanac.find_discrete(t0, t1, f)

        previous_e = f(t0).item()
        sky_transitions = {}
        for t, e in zip(times, events, strict=False):
            if previous_e < e:
                key = f"{almanac.TWILIGHTS[e]} starts"
                if "twilight starts" in key:
                    key = key.replace("twilight starts", "Dawn")
                if "Day starts" in key:
                    key = "Sunrise"
            else:
                key = f"{almanac.TWILIGHTS[previous_e]} ends"
                if "twilight ends" in key:
                    key = key.replace("twilight ends", "Dusk")
                if "Day ends" in key:
                    key = "Sunset"
            sky_transitions[key] = t.astimezone(zone)
            previous_e = e
        return sky_transitions
