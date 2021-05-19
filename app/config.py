"""
App Settings

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

# Standard Library
from functools import lru_cache
from typing import List

# Third Party
from pydantic import BaseSettings

# --------------------------------------------------------------


class DataBaseSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_db: str
    postgres_pwd: str
    connection_number: int
    nation: str

    class Config:

        """Location of the settings file."""

        env_file = ".env"


@lru_cache(maxsize=1)
def get_database_settings() -> DataBaseSettings:
    return DataBaseSettings()


# --------------------------------------------------------------


class SecuritySettings(BaseSettings):
    algorithm: str
    issuer: str
    audience: str
    realm_public_key: str
    realm_access: List[str]

    class Config:

        """Location of the settings file."""

        env_file = ".env"


@lru_cache(maxsize=1)
def get_security_settings() -> SecuritySettings:
    return SecuritySettings()
