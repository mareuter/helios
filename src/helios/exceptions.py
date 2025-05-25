# Copyright 2023-2025 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Module for program exceptions."""

from __future__ import annotations

__all__ = ["BadTimezone"]


class BadTimezone(Exception):
    """Exception for bad timezone."""

    pass
