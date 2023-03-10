# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = ["Helios"]

from datetime import datetime, timedelta
from importlib.resources import files

from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from skyfield import almanac
from skyfield.api import load, load_file, wgs84

from .exceptions import BadTimezone

DATA_PATH = files("app.skyfield").joinpath("de421.bsp")


class Helios:
    def __init__(self) -> None:
        self.timescale = load.timescale()
        self.ephemeris = load_file(DATA_PATH)

    def sky_transitions(
        self,
        latitude: float,
        longitude: float,
        current_datetime: datetime,
        location_timezone: str,
    ) -> dict[str, datetime]:
        """Calculates sky transitions.

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
        current_datetime : datetime
            The current date and time to calculate the sky transitions for.
            Only date is used.
        location_timezone : str
            The timezone for the location.

        Returns
        -------
        dict
            The object containing the name of the sky transition as the key
            and the sky transition date/time.
        """
        try:
            zone = timezone(location_timezone)
        except UnknownTimeZoneError:
            raise BadTimezone
        now = zone.localize(current_datetime)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)

        t0 = self.timescale.from_datetime(midnight)
        t1 = self.timescale.from_datetime(next_midnight)

        location = wgs84.latlon(latitude, longitude)
        f = almanac.dark_twilight_day(self.ephemeris, location)
        times, events = almanac.find_discrete(t0, t1, f)

        previous_e = f(t0).item()
        sky_transitions = {}
        for t, e in zip(times, events):
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
