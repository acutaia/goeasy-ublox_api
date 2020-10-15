#!/usr/bin/env python3
"""
App main entry point

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
# Standard Library
from functools import lru_cache
from typing import List

# Third Party
from fastapi import FastAPI, Path, Body, Depends
from fastapi.responses import ORJSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

# Internal
from .models.satellite import RawData, Satellite, SatelliteInfo
from .db.postgresql import DataBase
from .security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

auth = Signature()
database = DataBase()
app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/api/v1/galileo/docs", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="UbloxApi",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/satellite.png",
    )


@app.get(
    "/api/v1/galileo/request/{satellite_id}/{timestamp}",
    response_class=ORJSONResponse,
    response_model=RawData,
    summary="Extract Raw Data",
    response_description="Raw Data",
    tags=["Galileo"],
    dependencies=[Depends(auth)]
)
async def raw_data(
    satellite_id: int = Path(..., description="Id of the Satellite", example=36),
    timestamp: int = Path(..., description="Timestamp of the data to retrieve", example=1587506414)
):
    """
    Extract the Raw Data of a satellite in a specific timestamp

    - **satellite_id**: identification code of the satellite
    - **timestamp**: requested timestamp
    - **raw_data**: data sent by the satellite in that timestamp
    """
    return await database.extract_raw_data(satellite_id, timestamp)


@app.post(
    "/api/v1/galileo/request",
    response_class=ORJSONResponse,
    response_model=List[SatelliteInfo],
    summary="Extract Satellites Info",
    response_description="The raw data of the satellites in the specified timestamps",
    tags=["Galileo"],
    dependencies=[Depends(auth)]
)
async def satellites_info(satellites: List[Satellite] = Body(...)):
    """
    Extract the RaW Data of a satellites list in a specific timestamp

    - **satellite_id**: identification code of the satellite
    - **info**: list of requested timestamp
    - **raw_data**: data sent by the satellite in that timestamp
    """
    return await database.extract_satellites_info(satellites)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="UbloxApi",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo_full.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
