#!/usr/bin/env python3
"""
Satellite models package

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

# Standard Library
from typing import Optional, List

# Third Party
from pydantic import BaseModel, Field
import ujson

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

    class Config:
        """With this configuration we use ujson to improve performance"""
        json_loads = ujson.loads
        json_dumps = ujson.dumps


class GalileoData(RawData):
    """Model of Galileo Data of a Satellite"""
    raw_data: Optional[str] = Field(
        description="Galileo data in a specific timestamp",
        example="077677340100635d242251f57f0f40a66540000000002aaaaa57d23fbf40"
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

    class Config:
        """With this configuration we use ujson to improve performance"""
        json_loads = ujson.loads
        json_dumps = ujson.dumps


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


class Galileo(Satellite):
    """Model of a Galileo satellite """
    info: List[GalileoData] = Field(
        ...,
        description="List of requested Galileo Data in specifics timestamps",
        example=[
            GalileoData(timestamp=1613406498000)
        ]
    )


class GalileoInfo(Galileo):
    """Class used only for documentation"""
    info: List[GalileoData] = Field(
        ...,
        description="List of Galileo Data of in a specific timestamp",
        example=[
            GalileoData(
                timestamp=1613406498000,
                raw_data="077677340100635d242251f57f0f40a66540000000002aaaaa57d23fbf40"
            )
        ]
    )
