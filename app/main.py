# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = ["app"]

import math
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Query
from pydantic import BaseModel

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
    cdatetime: float,
    tz: str,
    lat: float = Query(
        le=math.fabs(90.0),
        title="latitude",
        description="The location's latitude. North is positive. South is negative",
    ),
    lon: float = Query(
        le=math.fabs(180.0),
        title="latitude",
        description="The location's latitude coordinate. East is positive. West is negative.",
    ),
) -> Any:
    h = Helios()
    st = h.sky_transitions(lat, lon, datetime.fromtimestamp(cdatetime), tz)
    output = {k.replace(" ", "_").lower(): v.timestamp() for k, v in st.items()}
    return output
