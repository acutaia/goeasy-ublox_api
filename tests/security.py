"""
Security Utilities for testing

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
from datetime import datetime, timedelta
import os
import uuid

# Third Party
import dotenv
from jose import jwt

# ------------------------------------------------------------------------------


# Module version
__version_info__ = (1, 0, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"


# ------------------------------------------------------------------------------


PATH = os.path.abspath(os.path.dirname(__file__))

with open(f"{PATH}/private.pem", "r") as fp:
    PRIVATE_KEY = fp.read()

with open(f"{PATH}/public.pem", "r") as fp:
    PUBLIC_KEY = fp.read()

ISSUER = "Travis-ci/test"
AUDIENCE = "Travis-ci/test"

# ------------------------------------------------------------------------------


def configure_security_for_testing():
    """Change JWT scope for testing purpose."""
    env_file = dotenv.find_dotenv()
    dotenv.load_dotenv(env_file)
    os.environ["REALM_ACCESS"] = '["Test"]'
    os.environ["AUDIENCE"] = AUDIENCE
    os.environ["ISSUER"] = ISSUER
    os.environ["REALM_PUBLIC_KEY"] = PUBLIC_KEY


def get_valid_token() -> str:
    """
    Generate a valid token using the private key associated to the public
    one both keys are used only for testing purpose."""
    to_encode = {
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() + timedelta(seconds=300),
        "iat": datetime.utcnow(),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "realm_access": {"roles": ["Test"]},
    }

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")


def get_invalid_token() -> str:
    """
    Generate a invalid token using the private key associated to the public
    one both keys are used only for testing purpose."""
    to_encode = {
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() - timedelta(seconds=300),
        "iat": datetime.utcnow() - timedelta(seconds=600),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "realm_access": {"roles": ["Test"]},
    }

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")
