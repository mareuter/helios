# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = ["Helios"]

from importlib.resources import files

from skyfield.api import load, load_file

DATA_PATH = files("app.skyfield").joinpath("de421.bsp")


class Helios:
    def __init__(self) -> None:
        self.timescale = load.timescale()
        self.ephemeris = load_file(DATA_PATH)
