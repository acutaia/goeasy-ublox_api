"""
Ublox Router

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2021 Angelo Cutaia

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

# Third Party
from fastapi import APIRouter, Depends, Path, Body
from fastapi.responses import UJSONResponse

# Internal
from ..models.satellite import RawData, Satellite, SatelliteInfo
from ..db.postgresql import get_database
from ..security.jwt_bearer import get_signature

# --------------------------------------------------------------------------------------------

# Instantiate
auth = get_signature()
database = get_database()

# Instantiate router
router = APIRouter(prefix="/api/v1/galileo/ublox", tags=["Ublox"])

# --------------------------------------------------------------------------------------------


@router.post(
    "/request",
    response_class=UJSONResponse,
    response_model=SatelliteInfo,
    summary="Extract Ublox Info",
    response_description="The Ublox data of the satellite in the specified timestamps",
    dependencies=[Depends(auth)],
)
async def ublox_info(satellite: Satellite = Body(...)):
    """
    Extract the Ublox Data of a satellite in a list of specific timestamps

    - **satellite_id**: identification code of the satellite
    - **info**: list of requested timestamp in ms
    - **raw_data**: data sent by the satellite in that timestamp
    """
    return await database.extract_satellite_info(satellite)


# --------------------------------------------------------------------------------------------


@router.get(
    "/request/{satellite_id}/{timestamp}",
    response_class=UJSONResponse,
    response_model=RawData,
    summary="Extract Ublox Data",
    response_description="Ublox Data",
    dependencies=[Depends(auth)],
)
async def ublox_data(
    satellite_id: int = Path(..., description="Id of the Satellite", example=36),
    timestamp: int = Path(
        ...,
        description="Timestamp in ms of the data to retrieve",
        example=1613406498000,
    ),
):
    """
    Extract the Ublox Data of a satellite in a specific timestamp

    - **satellite_id**: identification code of the satellite
    - **timestamp**: requested timestamp in ms
    - **raw_data**: data sent by the satellite in that timestamp
    """
    return await database.extract_raw_data(satellite_id, timestamp)


# --------------------------------------------------------------------------------------------
