# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import pathlib

from skyfield.api import Loader


def main() -> None:
    root = pathlib.Path(__file__).parents[1]
    load = Loader(root / "app" / "skyfield")
    load("de421.bsp")


if __name__ == "__main__":
    main()
