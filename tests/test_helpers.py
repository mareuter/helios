# Copyright 2023-2025 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for helpers."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

from helios.helpers import get_time_variation


def test_get_time_variation() -> None:
    variation = -timedelta(seconds=160)
    with patch("helios.helpers.random.randrange", return_value=variation.seconds):
        value = get_time_variation("0:06:00")
        assert value.seconds == variation.seconds
