import httpx
from fastapi import HTTPException
import json

class AuthServiceClientFactory:
    def __init__(self, base_url: str, token_url: str):
        self.base_url = base_url
        self.token_url = token_url

    def create_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url)

    async def post(
        self, endpoint: str, data: dict | None = None, headers: dict | None = None
    ) -> httpx.Response:
        async with self.create_client() as client:
            try:
                response = await client.post(endpoint, json=data, headers=headers)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                status_code = int(exc.response.status_code)
                try:
                    error = exc.response.json()
                except (ValueError, Exception):
                    error = exc.response.text
                raise HTTPException(status_code=status_code, detail=error)
