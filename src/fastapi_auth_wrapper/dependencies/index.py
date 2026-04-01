from typing import Annotated

from fastapi import Depends, Header
from fastapi.exceptions import HTTPException

from fastapi_auth_wrapper.clients import AuthServiceClient, get_service_client


async def authorization_service_dependency(
    authorization: str = Header(None, alias="Authorization"),
    client: AuthServiceClient = Depends(get_service_client),
) -> AuthServiceClient:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization Header required")

    try:
        scheme, token = authorization.split(" ")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid header format") from e

    if not (scheme.lower() == "bearer"):
        raise HTTPException(
            status_code=401, detail="Invalid token scheme: Expected Bearer"
        )
    response = await client.validate_user_token(token)
    client.user = response
    return client


AuthorizedUserClient = Annotated[
    AuthServiceClient, Depends(authorization_service_dependency)
]
