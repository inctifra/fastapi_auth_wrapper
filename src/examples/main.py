from fastapi import FastAPI
from fastapi_auth_wrapper import AuthorizedUserClient


app = FastAPI()


@app.get("/check")
async def get_status(client: AuthorizedUserClient):
    print(client.user)
    return {}
