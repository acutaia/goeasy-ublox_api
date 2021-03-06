"""
Test the app.database package

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0

..

    Copyright 2021 LINKS Foundation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Third party
import uvloop
import pytest

# DataBase
from .postgresql import (
    FakeDatabase,
    raw_data,
    timestampMessage_unix,
    raw_svId,
    galileo_data,
)
from app.db.postgresql import DataBase

# Satellites
from app.models.satellite import Satellite, RawData, Galileo, GalileoData

# ------------------------------------------------------------------------------


# Module version
__version_info__ = (1, 0, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"


# ------------------------------------------------------------------------------


@pytest.fixture()
def event_loop():
    """Set uvloop as the default event loop."""
    loop = uvloop.Loop()
    yield loop
    loop.close()


class TestDatabase:
    """Test the postgresql module."""

    @pytest.mark.asyncio
    async def test_extract_raw_data(self):
        """Test the extraction of raw_data from the database."""

        # Setup the Database
        await FakeDatabase.create_database()
        # Connect to the Database
        await DataBase.connect()

        # Try to extract data that are inside in the db
        data = await DataBase.extract_raw_data(raw_svId, timestampMessage_unix)
        assert raw_data == data["raw_data"], "Raw Data should be equal"

        # Try to extract data that aren't inside the db
        data = await DataBase.extract_raw_data(raw_svId, timestampMessage_unix + 4000)
        assert data["raw_data"] is None, "Raw Data should be none"
        data = await DataBase.extract_raw_data(raw_svId + 1, timestampMessage_unix)
        assert data["raw_data"] is None, "Raw Data should be none"

        # Disconnect from the Database
        await DataBase.disconnect()

    @pytest.mark.asyncio
    async def test_extract_galileo_data(self):
        """Test the extraction of galileo_data from the database."""

        # Setup the Database
        await FakeDatabase.create_database()
        # Connect to the Database
        await DataBase.connect()

        # Try to extract data that are inside in the db
        data = await DataBase.extract_galileo_data(raw_svId, timestampMessage_unix)
        assert galileo_data == data["raw_data"], "Galileo Data should be equal"

        # Try to extract data that aren't inside the db
        data = await DataBase.extract_galileo_data(
            raw_svId, timestampMessage_unix + 4000
        )
        assert data["raw_data"] is None, "Galileo Data should be none"
        data = await DataBase.extract_galileo_data(raw_svId + 1, timestampMessage_unix)
        assert data["raw_data"] is None, "Galileo Data should be none"

        # Disconnect from the Database
        await DataBase.disconnect()

    @pytest.mark.asyncio
    async def test_extract_satellite_info(self):
        """Test the extraction of Satellite Info."""

        # Setup the Database
        await FakeDatabase.create_database()
        # Connect to the Database
        await DataBase.connect()

        # Fake satellite requested raw_data
        satellite = Satellite(
            satellite_id=raw_svId,
            info=[
                RawData(timestamp=timestampMessage_unix),
                RawData(timestamp=timestampMessage_unix + 4000),
            ],
        )
        # Try to extract satellites info from the db
        satellite_info = await DataBase.extract_satellite_info(satellite)

        assert raw_data == satellite_info["info"][0].raw_data, "Raw Data must be equal"
        assert satellite_info["info"][1].raw_data is None, "Raw Data must be None"

        # Disconnect from the Database
        await DataBase.disconnect()

    @pytest.mark.asyncio
    async def test_extract_galileo_info(self):
        """Test the extraction of Galileo Info."""

        # Setup the Database
        await FakeDatabase.create_database()
        # Connect to the Database
        await DataBase.connect()

        # Fake satellite requested raw_data
        satellite = Galileo(
            satellite_id=raw_svId,
            info=[
                GalileoData(timestamp=timestampMessage_unix),
                GalileoData(timestamp=timestampMessage_unix + 4000),
            ],
        )
        # Try to extract satellites info from the db
        galileo_info = await DataBase.extract_galileo_info(satellite)

        assert (
            galileo_data == galileo_info["info"][0].raw_data
        ), "Raw Data must be equal"
        assert galileo_info["info"][1].raw_data is None, "Raw Data must be None"

        # Disconnect from the Database
        await DataBase.disconnect()
