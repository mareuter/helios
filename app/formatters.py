# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from datetime import datetime


def date_format(date: datetime) -> str:
    """Format date to Month Name Day, Year

    Parameters
    ----------
    date : datetime
        The current date/time to format.

    Returns
    -------
    str
        The formatted date string.
    """
    return date.strftime("%B %-d, %Y")
