from typing import Any

from fastapi import Depends
from fastapi.exceptions import HTTPException as HttpException

from fastapi_auth_wrapper.config import get_settings_dep, settings

from .factory import AuthServiceClientFactory


class AuthServiceClient(AuthServiceClientFactory):
    def __init__(self, settings: settings.Settings):
        super().__init__(
            base_url=settings.auth_service_url,
            token_url=settings.auth_service_token_url,
        )
        self.user: dict = {}

    async def validate_user_token(self, token: str) -> Any:
        try:
            response = await self.post(
                self.token_url,
                data={},
                headers={"Authorization": f"Bearer {token}"},
            )
            return response.json()
        except Exception as e:
            raise HttpException(status_code=401, detail=str(e)) from e


def get_service_client(
    settings: settings.Settings = Depends(get_settings_dep),
) -> AuthServiceClient:
    return AuthServiceClient(settings)
