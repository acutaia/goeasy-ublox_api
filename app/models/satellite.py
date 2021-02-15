#!/usr/bin/env python3
"""
Satellite models package

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
from typing import Optional, List
# Third Party
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------------------


class RawData(BaseModel):
    """Model of Raw Data of a Satellite"""
    timestamp: int = Field(
        ...,
        description="Timestamp in ms of the data to retrieve",
        example=1613406498000
    )
    raw_data: Optional[str] = Field(
        description="Data of the Satellite in a specific timestamp",
        example="02132c000224010009080200afe20702188a1e3ce838b8d80000fa90004037842a000000f377aaaa00403fdabdaaaa2ac260"
    )


class Satellite(BaseModel):
    """Model of a Satellite"""
    satellite_id: int = Field(
        ...,
        description="id of the satellite",
        example=36
    )
    info: List[RawData] = Field(
        ...,
        description="List of requested Raw Data in specifics timestamps",
        example=[
            RawData(timestamp=1613406498000)
        ]
    )


class SatelliteInfo(Satellite):
    """Class used only for documentation"""
    info: List[RawData] = Field(
        ...,
        description="List of Raw Data of the satellite in a specific timestamp",
        example=[
            RawData(
                timestamp=1613406498000,
                raw_data="02132c000224010009080200afe20702188a1e3ce838b8d80000fa90004037842a000000f377aaaa00403fdabdaaaa2ac260"
            )
        ]
    )
