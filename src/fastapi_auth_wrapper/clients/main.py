from .factory import AuthServiceClientFactory
from fastapi_auth_wrapper.config import settings
from typing import Any
from fastapi.exceptions import HTTPException as HttpException


class AuthServiceClient(AuthServiceClientFactory):
    def __init__(
        self,
        base_url: str = settings.auth_service_url,
        token_url: str = settings.auth_service_token_url,
    ):
        super().__init__(base_url, token_url)
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


def get_service_client() -> AuthServiceClient:
    return AuthServiceClient()
