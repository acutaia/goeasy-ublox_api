#!/usr/bin/env python3
"""
Asynchronous database

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

# Standard library
import asyncio
import time

# Asynchronous libraries
import asyncpg
from uvloop import Loop

# Database
from app.config import get_database_settings

# ------------------------------------------------------------------------------


# Module version
__version_info__ = (1, 0, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"


# ------------------------------------------------------------------------------


########
# TIME #
########

raw_galTow = 379328
"""Galielo time of the week"""

raw_galWno = 1073
"""Galielo week number"""

raw_leapS = 18
"""Galileo leap seconds"""

timestampMessage_unix = 1584609710
"""Time stamp of the message in a unix system"""

timestampMessage_galileo = 649329725
"""Time stamp of the message in galileo"""

time_raw_ck_A = 163
"""Time checksum A"""

time_raw_ck_B = 239
"""Time checksum B"""

# ------------------------------------------------------------------------------


###########
# GALILEO #
###########


raw_data = bytes(
    [
        0x2, 0x13, 0x2C, 0x0, 0x2, 0x12, 0x1, 0x0, 0x9, 0xE, 0x2, 0xD2, 0x34, 0x77, 0x76, 0x7,
        0x5D, 0x63, 0x0, 0x1, 0xF5, 0x51, 0x22, 0x24, 0x0, 0x40, 0xF, 0x7F, 0x0, 0x40, 0x65,
        0xA6, 0x2A, 0x0, 0x0, 0x0, 0xD2, 0x57, 0xAA, 0xAA, 0x0, 0x40, 0xBF, 0x3F, 0xD5, 0x9A,
        0xE8, 0x3F, 0x4A, 0x7C
    ]
).hex()
"""Galileo message raw_data"""

raw_auth = 0
"""Int value of the 5 authorization bytes"""

raw_svId = 18
"""Galielo service id"""

raw_numWords = 9
"""Num of words"""

raw_ck_A = 74
"""Galileo checksum A"""

raw_ck_B = 124
"""Galileo checksum B"""

# ------------------------------------------------------------------------------


#################
# DATA TO STORE #
#################


DATA_TO_STORE = (
    time.time(),
    timestampMessage_unix,
    raw_galTow,
    raw_galWno,
    raw_leapS,
    raw_data,
    0,
    raw_svId,
    raw_numWords,
    raw_ck_B,
    raw_ck_A,
    time_raw_ck_A,
    time_raw_ck_B,
    timestampMessage_galileo
)
"""Data to use to test the database"""


############
# DATABASE #
############


class FakeDatabase:
    """
    A class that handles a test database.
    The scope of this class is to build the database and save data inside it
    using a connection pool
    """
    settings = get_database_settings()
    """Database Settings"""

    pool: asyncpg.pool.Pool = None
    """Connection pool"""

    @classmethod
    async def create_database(cls) -> None:
        """
        Create a test database.
        """
        try:
            # create a connection pool
            cls.pool = await asyncpg.create_pool(
                host=cls.settings.postgres_host,
                port=cls.settings.postgres_port,
                user=cls.settings.postgres_user,
                password=cls.settings.postgres_pwd,
                database=cls.settings.postgres_db
            )

        except asyncpg.InvalidCatalogNameError:
            # Database does not exist, create it

            # create a single connection to the default user and the database template
            sys_conn = await asyncpg.connect(
                host=cls.settings.postgres_host,
                user=cls.settings.postgres_user,
                port=cls.settings.postgres_port,
                password=cls.settings.postgres_pwd,
                database="template1",
            )
            # create the database
            await sys_conn.execute(
                f'CREATE DATABASE "{cls.settings.postgres_db}" OWNER "{cls.settings.postgres_user}";'
            )
            # close the connection
            await sys_conn.close()

            # Setup the test database and fill with fake data.
            await cls.create_database()
            await cls.store_data(DATA_TO_STORE)
            await cls.pool.close()

    @classmethod
    async def store_data(cls, data_to_store: tuple) -> None:
        """
        Use a connection from the pool to insert the data in the db
        and check if the insertion is successful then release the
        connection. If the table in which the data must be stored doesn't
        exist, it will create it. In case all the connections in the pool are busy,
        await for a connection to be free.

        :param data_to_store:
        :return:
        """
        table = f"2020_Italy_{raw_svId}"
        try:
            # Take a connection from the pool and execute the query
            await cls.pool.execute(
                f'''
                INSERT INTO "{table}" (
                receptiontime,
                timestampmessage_unix,
                raw_galtow,
                raw_galwno,
                raw_leaps,
                raw_data,
                raw_authbit,
                raw_svid,
                raw_numwords,
                raw_ck_b,
                raw_ck_a,
                raw_ck_a_time,
                raw_ck_b_time,
                timestampmessage_galileo
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);''',
                *data_to_store
            )

        # Check if the table does'nt exist
        except asyncpg.UndefinedTableError:
            # Log the error code

            # Create the table
            async with cls.pool.acquire() as con:
                await con.execute(
                    f'''
                        CREATE TABLE IF NOT EXISTS "{table}" (
                        receptiontime bigint,
                        timestampmessage_unix bigint,
                        PRIMARY KEY (timestampmessage_unix),
                        raw_galtow integer,
                        raw_galwno integer,
                        raw_leaps integer,
                        raw_data text,
                        raw_authbit bigint,
                        raw_svid integer,
                        raw_numwords integer,
                        raw_ck_b integer,
                        raw_ck_a integer,
                        raw_ck_a_time integer,
                        raw_ck_b_time integer,
                        timestampmessage_galileo bigint
                        );
                         '''
                )

                # Create a index for the table
                await con.execute(
                    f'''CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_timestampmessage_unix on "{table}"
                     (timestampmessage_unix DESC NULLS LAST);'''
                    )

            # store data in the new table
            await cls.store_data(data_to_store)
