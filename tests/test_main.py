# Copyright 2023-2024 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for application routes."""

from __future__ import annotations

import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from helios.main import app
import pytest

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "This is a web service, nothing to see here."}


def test_sky_transitions() -> None:
    response = client.get(
        "/sky_transitions",
        params={
            "lat": 40.8939,
            "lon": -83.8917,
            "cdatetime": 1677880560.0,
            "tz": "US/Eastern",
        },
    )
    assert response.status_code == 200
    assert response.json()["astronomical_dawn"] == pytest.approx(1677839749.146742, rel=1e-1)


def test_bad_location() -> None:
    response = client.get(
        "/sky_transitions",
        params={
            "lat": 96.5,
            "lon": 184.342,
            "cdatetime": 1677880560.0,
            "tz": "US/Eastern",
        },
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    for info in detail:
        if "lat" in info["loc"]:
            assert info["msg"] == "Input should be less than or equal to 90"
        if "lon" in info["loc"]:
            assert info["msg"] == "Input should be less than or equal to 180"


def test_bad_timezone() -> None:
    response = client.get(
        "/sky_transitions",
        params={
            "lat": 40.8939,
            "lon": -83.8917,
            "cdatetime": 1677880560.0,
            "tz": "USA/Santiago",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Bad time zone given: USA/Santiago"


def test_day_information() -> None:
    utc = datetime.datetime(2023, 3, 3, 19, 56, 0, tzinfo=datetime.UTC)
    with patch("helios.solar_calculator.SolarCalculator.get_utc", return_value=utc):
        response = client.get(
            "/day_information",
            params={
                "lat": 40.8939,
                "lon": -83.8917,
                "cdatetime": 1677880560.0,
                "tz": "US/Eastern",
            },
        )
        assert response.status_code == 200
        assert response.template.name == "day_information.html"
        assert "request" in response.context
        assert "Sun Information for March 3, 2023" in response.text
        assert "Astronomical Dawn" in response.text


def test_timer_information() -> None:
    utc = datetime.datetime(2023, 3, 3, 19, 56, 0, tzinfo=datetime.UTC)
    variations = [-200, 510]
    with (
        patch("helios.solar_calculator.SolarCalculator.get_utc", return_value=utc),
        patch("helios.helpers.random.randrange", side_effect=variations),
    ):
        response = client.get(
            "/timer_information",
            params={
                "lat": 40.8939,
                "lon": -83.8917,
                "cdatetime": 1677880560.0,
                "tz": "US/Eastern",
                "checktime": "00:10:00",
                "offtime": "22:00:00",
                "onrange": "0:05:00",
                "offrange": "0:10:00",
            },
        )
        assert response.status_code == 200
        output = response.json()
        assert output["date"] == "March 3, 2023"
        assert output["check_time_utc"] == 1677906600
        assert output["sunrise_usno"] == "07:07"
        assert output["sunset_usno"] == "18:29"
        assert output["on_time_utc"] == 1677885923
        assert output["on_time"] == "18:25:23"
        assert output["off_time_utc"] == 1677899310
        assert output["off_time"] == "22:08:30"
