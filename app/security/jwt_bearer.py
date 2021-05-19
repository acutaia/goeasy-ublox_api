"""
JWT_BEARER  package

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
from datetime import timedelta, datetime
from functools import lru_cache, wraps

# Third Party
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# Internal
from ..config import get_security_settings

# --------------------------------------------------------------------------------------------


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """
    Decorator that turn the LruCache in a TLRUCache

    :param seconds: duration of the cache
    :param maxsize: number of element stored in the cache (works  better when maxsize is a power-of-two)
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache


@timed_lru_cache(180, maxsize=16)
def _jwt_decode(jwt_token: str):
    """
    Checks if a token is valid or not

    :param jwt_token: token to check
    """
    settings = get_security_settings()
    try:
        jwt.decode(
            jwt_token,
            f"-----BEGIN PUBLIC KEY-----\n"
            f"{settings.realm_public_key}"
            f"\n-----END PUBLIC KEY-----"
            "",
            settings.algorithm,
            issuer=settings.issuer,
            audience=settings.audience,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
        )


class Signature(HTTPBearer):
    async def __call__(self, request: Request) -> None:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        jwt_token = credentials.credentials
        _jwt_decode(jwt_token)


@lru_cache(maxsize=1)
def get_signature() -> Signature:
    return Signature()
