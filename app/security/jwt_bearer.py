from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from ..config import get_security_settings


class Signature(HTTPBearer):
    async def __call__(self, request: Request) -> None:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
            )

        jwt_token = credentials.credentials
        settings = get_security_settings()
        try:
            jwt.decode(
                jwt_token,
                f"-----BEGIN PUBLIC KEY-----\n"
                f"{settings.realm_public_key}"
                f"\n-----END PUBLIC KEY-----""",
                settings.algorithm,
                issuer=settings.issuer,
                audience=settings.audience
            )
        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
            )

