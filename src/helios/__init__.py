# Copyright 2023-2025 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = [
    "__author__",
    "__email__",
    "__version__",
    "version_info",
]

from importlib.metadata import PackageNotFoundError, version

__author__ = "Michael Reuter"
__email__ = "mareuternh@gmail.com"
try:
    __version__ = version("helios")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"

version_info = __version__.split(".")
"""The decomposed version, split across "``.``."

Use this for version comparison.
"""
