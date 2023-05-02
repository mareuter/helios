# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

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
    assert response.json()["astronomical_dawn"] == pytest.approx(
        1677839749.146742, rel=1e-1
    )


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
            assert info["msg"] == "ensure this value is less than or equal to 90.0"
        if "lon" in info["loc"]:
            assert info["msg"] == "ensure this value is less than or equal to 180.0"


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
    utc = datetime.datetime(2023, 3, 3, 19, 56, 0, tzinfo=datetime.timezone.utc)
    with patch("app.helios.Helios.get_utc", return_value=utc):
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
