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
from httpx import AsyncClient
import pytest
import uvloop

# Internal
from .security import INVALID_TOKEN, configure_security_for_testing, get_valid_token
from app.main import app

# ------------------------------------------------------------------------------


# Module version
__version_info__ = (1, 0, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"


# ------------------------------------------------------------------------------

configure_security_for_testing()
"""Configure the app for testing purpose"""


@pytest.yield_fixture()
def event_loop():
    """
    Set uvloop as the default event loop
    """
    loop = uvloop.Loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_docs():
    async with AsyncClient(app=app, base_url="http://localhost:8080/api/v1/galileo/") as ac:
        response = await ac.get("/docs")
    assert response.status_code == 200
