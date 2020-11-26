#!/usr/bin/env python3
"""
App Tests

:author: Angelo Cutaia
:copyright: Copyright 2020, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Third party
from fastapi.testclient import TestClient
import orjson
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

# Internal
from .postgresql import raw_svId, timestampMessage_unix, raw_data
from .security import INVALID_TOKEN, configure_security_for_testing, get_valid_token
from app.main import app, RawData, Satellite, SatelliteInfo

# ------------------------------------------------------------------------------


# Module version
__version_info__ = (1, 0, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"


# ------------------------------------------------------------------------------

configure_security_for_testing()
"""Configure the app for testing purpose"""

def test_docs():
    """
    Test the documentation of ublox_api
    """
    with TestClient(app=app) as client:
        response = client.get(url="/api/v1/galileo/docs")
        assert response.status_code == 200


def test_raw_data():
    """
    Test the endpoint used to get the raw_data"
    """

    with TestClient(app=app) as client:
        # Try to get info without a Token
        response = client.get(
            url=f"/api/v1/galileo/request/{raw_svId}/{timestampMessage_unix}"
        )
        assert response.status_code == HTTP_403_FORBIDDEN, "Authentication is based on JWT"

        # Try to get info with an invalid Token
        response = client.get(
            url=f"/api/v1/galileo/request/{raw_svId}/{timestampMessage_unix}",
            headers={
                "Authorization": f"Bearer {INVALID_TOKEN}"
            }
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED, "Token not Valid"

        # Obtain a valid Token and try to get info
        valid_token = get_valid_token()
        response = client.get(
            url=f"/api/v1/galileo/request/{raw_svId}/{timestampMessage_unix}",
            headers={"Authorization": f"Bearer {valid_token}"
                     }
        )
        assert response.status_code == 200, "The token must be valid"
        assert response.json() == {
            "timestamp": timestampMessage_unix,
            "raw_data": raw_data
        }, "Error during the extraction of data from the database"


def test_satellites_info():
    """
    Test the endpoint that gives the satellites info
    """
    with TestClient(app=app) as client:
        # Try to get info without a Token
        response = client.post(
            url=f"/api/v1/galileo/request",
            data=orjson.dumps(
                [
                    {
                        "satellite_id": raw_svId,
                        "info": [
                            {
                                "timestamp": timestampMessage_unix
                            }
                        ]
                    }
                ]
            )
        )

        assert response.status_code == HTTP_403_FORBIDDEN, "Authentication is based on JWT"

        # Try to get info with an invalid Token
        response = client.post(
            url=f"/api/v1/galileo/request",
            data=orjson.dumps(
                [
                    {
                        "satellite_id": raw_svId,
                        "info": [
                            {
                                "timestamp": timestampMessage_unix
                            }
                        ]
                    }
                ]
            ),
            headers={
                "Authorization": f"Bearer {INVALID_TOKEN}"
            }
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED, "Token not Valid"

        # Obtain a valid Token and try to get info
        valid_token = get_valid_token()
        response = client.post(
            url=f"/api/v1/galileo/request",
            data=orjson.dumps(
                [
                    {
                        "satellite_id": raw_svId,
                        "info": [
                            {
                                "timestamp": timestampMessage_unix
                            }
                        ]
                    }
                ]
            ),
            headers={"Authorization": f"Bearer {valid_token}"
                     }
        )
        assert response.status_code == 200, "The token must be valid"

        assert response.json()[0] == SatelliteInfo(
            satellite_id=raw_svId,
            info=[
                RawData(
                    timestamp=timestampMessage_unix,
                    raw_data=raw_data
                )
            ]
        ).dict(), "Error during the extraction of data from the database"





