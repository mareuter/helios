# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Script for downloading ephemeris data."""

import pathlib

from skyfield.api import Loader


def main() -> None:
    """Download ephemeris data."""
    root = pathlib.Path(__file__).parents[1]
    load = Loader(root / "src" / "helios" / "skyfield")
    load("de421.bsp")


if __name__ == "__main__":
    main()
