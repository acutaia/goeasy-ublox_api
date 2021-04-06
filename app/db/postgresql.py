"""
Database utility functions

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

# Standard library
from datetime import datetime
from functools import lru_cache
from typing import Optional

# Third party
from asyncpg import Connection, create_pool
from asyncpg.pool import Pool
from asyncpg.exceptions import UndefinedTableError

# Internal
from ..models.satellite import Satellite, Galileo

from ..config import get_database_settings

# ---------------------------------------------------------------------------------------


class DataBase:
    pool: Pool = None
    nation: str = None
    attack_on_reference_system: str = "AttackOnReferenceSystem"

    @classmethod
    async def connect(cls) -> None:
        settings = get_database_settings()
        cls.pool = await create_pool(
            user=settings.postgres_user,
            password=settings.postgres_pwd,
            database=settings.postgres_db,
            host=settings.postgres_host,
            port=settings.postgres_port,
            min_size=settings.connection_number,
            max_size=settings.connection_number,
        )
        cls.nation = settings.nation

    @classmethod
    async def disconnect(cls):
        await cls.pool.close()

    @classmethod
    async def extract_satellite_info(cls, satellite: Satellite) -> dict:
        """Extract all the raw data of the satellites list.

        :param satellite: Satellite Id with the list of the timestamp of the data to retrieve
        :return: The info required for a specific Satellite
        """
        async with cls.pool.acquire() as conn:
            for raw_data in satellite.info:
                raw_data.raw_data = await cls._extract_data(
                    conn, satellite.satellite_id, raw_data.timestamp
                )

        return {"satellite_id": satellite.satellite_id, "info": satellite.info}

    @classmethod
    async def extract_raw_data(cls, satellite_id: int, timestamp: int) -> dict:
        """Extract Raw data of the Satellite in a specific timestamp.

        :param satellite_id: Satellite id
        :param timestamp: Timestamp of the raw data to retrieve
        :return: Raw Data of the satellite in the required timestamp
        """
        async with cls.pool.acquire() as conn:
            return {
                "timestamp": timestamp,
                "raw_data": await cls._extract_data(conn, satellite_id, timestamp),
            }

    @classmethod
    async def _extract_data(
        cls, conn: Connection, satellite_id: int, timestamp: int
    ) -> Optional[str]:
        """Utility function to extract data from the database.

        :param conn: A connection to the database
        :param satellite_id: Id of the satellite
        :param timestamp: Of the data to retrieve
        :return: The Raw Data of the Satellite in the specified timestamp
        """
        try:
            return await conn.fetchval(
                f"SELECT (CASE WHEN osnma = 0 THEN '{cls.attack_on_reference_system}' ELSE raw_data END)"
                f'FROM "{datetime.fromtimestamp(int(timestamp/1000)).year}_{cls.nation}_{satellite_id}" '
                f"WHERE timestampmessage_unix "
                f"BETWEEN {timestamp - 1000} AND {timestamp + 1000};"
            )

        except UndefinedTableError:
            # No raw_data found
            return None

    @classmethod
    async def extract_galileo_info(cls, satellite: Galileo) -> dict:
        """Extract all the raw data of the satellites list.

        :param satellite: Satellite Id with the list of the timestamp of the data to retrieve
        :return: The info required for a specific Satellite
        """
        async with cls.pool.acquire() as conn:
            for raw_data in satellite.info:
                raw_data.raw_data = await cls._extract_galileo_data(
                    conn, satellite.satellite_id, raw_data.timestamp
                )

        return {"satellite_id": satellite.satellite_id, "info": satellite.info}

    @classmethod
    async def extract_galileo_data(cls, satellite_id: int, timestamp: int) -> dict:
        """Extract Raw data of the Satellite in a specific timestamp.

        :param satellite_id: Satellite id
        :param timestamp: Timestamp of the raw data to retrieve
        :return: Galileo Data of the satellite in the required timestamp
        """
        async with cls.pool.acquire() as conn:
            return {
                "timestamp": timestamp,
                "raw_data": await cls._extract_galileo_data(
                    conn, satellite_id, timestamp
                ),
            }

    @classmethod
    async def _extract_galileo_data(
        cls, conn: Connection, satellite_id: int, timestamp: int
    ) -> Optional[str]:
        """Utility function to extract data from the database.

        :param conn: A connection to the database
        :param satellite_id: Id of the satellite
        :param timestamp: Of the data to retrieve
        :return: The Galileo Data of the Satellite in the specified timestamp
        """
        try:
            return await conn.fetchval(
                f"SELECT (CASE WHEN osnma = 0 THEN '{cls.attack_on_reference_system}' ELSE galileo_data END)"
                f'FROM "{datetime.fromtimestamp(int(timestamp / 1000)).year}_{cls.nation}_{satellite_id}" '
                f"WHERE timestampmessage_unix "
                f"BETWEEN {timestamp - 1000} AND {timestamp + 1000};"
            )

        except UndefinedTableError:
            # No raw_data found
            return None


@lru_cache(maxsize=1)
def get_database() -> DataBase:
    return DataBase()


# ---------------------------------------------------------------------------------------
