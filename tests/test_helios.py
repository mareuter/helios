# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from app.helios import Helios


def test_internal_parameters() -> None:
    h = Helios()
    assert h.ephemeris is not None
    assert h.timescale is not None
