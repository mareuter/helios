# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = ["app"]

import math
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel

from .exceptions import BadTimezone
from .helios import Helios

app = FastAPI()


class SkyTransitions(BaseModel):
    astronomical_dawn: float
    nautical_dawn: float
    civil_dawn: float
    sunrise: float
    sunset: float
    civil_dusk: float
    nautical_dusk: float
    astronomical_dusk: float


@app.get("/")
async def root() -> dict:
    return {"msg": "This is a web service, nothing to see here."}


@app.get("/sky_transitions")
async def sky_transitions(
    cdatetime: float = Query(
        title="current_datetime_timestamp",
        description="The UNIX timestamp for the current date/time.",
    ),
    tz: str = Query(
        title="timezone",
        description="The time zone associated with the current date/time.",
    ),
    lat: float = Query(
        le=math.fabs(90.0),
        title="latitude",
        description="The location's latitude coordinate. North is positive. South is negative",
    ),
    lon: float = Query(
        le=math.fabs(180.0),
        title="longitude",
        description="The location's longtude coordinate. East is positive. West is negative.",
    ),
) -> Any:
    h = Helios()
    try:
        st = h.sky_transitions(lat, lon, datetime.fromtimestamp(cdatetime), tz)
    except BadTimezone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bad time zone given: {tz}",
        )
    output = {k.replace(" ", "_").lower(): v.timestamp() for k, v in st.items()}
    return output
