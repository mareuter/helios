# Copyright 2023-2025 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Main application definition."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from importlib.resources import files
import math
from typing import Any
import zoneinfo

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import __version__
from .exceptions import BadTimezone
from .formatters import date_format, day_length_format, time_format
from .helpers import get_time_variation
from .models import TimerInformation
from .solar_calculator import SolarCalculator

__all__ = ["app"]

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(files("helios.data").joinpath("static"))), name="static")
templates = Jinja2Templates(directory=str(files("helios.data").joinpath("templates")))


def set_schema() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Helios Web Service API",
        version=__version__,
        description=" ".join(
            [
                "This API provides sky transition information for the sun ",
                "a templated page with the same information and a way to ",
                "gather information for a timer.",
            ]
        ),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = set_schema  # type: ignore


@app.get("/")
async def root() -> dict[str, str]:
    return {"msg": "This is a web service, nothing to see here."}


@app.get("/favicon.ico")
async def favicon() -> FileResponse:
    file_name = "helios.png"
    file_path = str(files("helios.data.static").joinpath(file_name))
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


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
    h = SolarCalculator()
    try:
        st = h.sky_transitions(lat, lon, cdatetime, tz)
    except BadTimezone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bad time zone given: {tz}",
        ) from None
    output = {k.replace(" ", "_").lower(): v.timestamp() for k, v in st.items()}
    return output


@app.get("/day_information", response_class=HTMLResponse)
async def day_information(
    request: Request,
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
    h = SolarCalculator()
    utctime = h.get_utc().timestamp()
    localtime = h.get_localtime(tz, utctime)
    try:
        st = h.sky_transitions(lat, lon, utctime, tz)
    except BadTimezone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bad time zone given: {tz}",
        ) from None
    output = {k.replace(" ", "_").lower(): time_format(v) for k, v in st.items()}
    day_length = st["Sunset"] - st["Sunrise"]
    return templates.TemplateResponse(
        request,
        "day_information.html",
        {
            "date": date_format(localtime),
            **output,
            "day_length": day_length_format(day_length),
        },
    )


@app.get("/timer_information")
async def timer_information(
    cdatetime: float = Query(
        title="current_datetime_timestamp",
        description="The UNIX timestamp for the current date/time in UTC.",
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
    checktime: str = Query(title="check_time", description="The local time for checking in HH:MM:SS"),
    offtime: str = Query(title="off_time", description="The local time for the off time in HH:MM:SS"),
    onrange: str = Query(
        title="on_range", description="Half of time range to be added to the on time in HH:MM:SS"
    ),
    offrange: str = Query(
        title="off_range", description="Half of time range to be added to the off time in HH:MM:SS"
    ),
) -> TimerInformation:
    h = SolarCalculator()
    localtime = h.get_localtime(tz, cdatetime)
    try:
        st = h.sky_transitions(lat, lon, cdatetime, tz)
    except BadTimezone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bad time zone given: {tz}",
        ) from None

    timezone = zoneinfo.ZoneInfo(tz)
    next_day = localtime.date() + timedelta(days=1)
    check_time = datetime.combine(next_day, datetime.strptime(checktime, "%H:%M:%S").time(), tzinfo=timezone)
    off_time = datetime.combine(
        localtime.date(), datetime.strptime(offtime, "%H:%M:%S").time(), tzinfo=timezone
    )

    on_variation = get_time_variation(onrange)
    off_variation = get_time_variation(offrange)

    off_time += off_variation
    on_time = st["Sunset"] + on_variation

    ti = TimerInformation(
        date=date_format(localtime),
        check_time_utc=int(check_time.astimezone(UTC).timestamp()),
        sunrise_usno=time_format(st["Sunrise"]),
        sunset_usno=time_format(st["Sunset"]),
        sunset_utc=int(st["Sunset"].astimezone(UTC).timestamp()),
        on_time_utc=int(on_time.astimezone(UTC).timestamp()),
        on_time=on_time.strftime("%H:%M:%S"),
        off_time_utc=int(off_time.astimezone(UTC).timestamp()),
        off_time=off_time.strftime("%H:%M:%S"),
    )
    return ti
