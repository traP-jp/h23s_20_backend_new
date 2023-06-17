"""
import json
from typing import Any, Union
import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from pydantic import BaseModel
import requests
from binascii import hexlify
from os import urandom

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=hexlify(urandom(32)).decode())

oauth = OAuth()
oauth.register(
    name="traq",
    client_id="bmLpJkCgkcPuQKedUIRpWFee7EE7zXSsIHpp",
    client_secret="HVoKtKIqp7tmnQ1YiTr0uK0PvzgnUKZsZHFn",
    access_token_url="https://q.trap.jp/api/v3/oauth2/token",
    access_token_params={"grant_type": "authorization_code"},
    authorize_url="https://q.trap.jp/api/v3/oauth2/authorize",
    authorize_params=None,
    api_base_url="https://q.trap.jp/api/v3",
    # client_kwargs={"timeout": Timeout(10.0)},
)

app_oauth = oauth.create_client("traq")


@app.get("/callback")
async def callback(request: Request):
    token = await app_oauth.authorize_access_token(request)

    return


@app.get("/login", response_model=None)
async def login(request: Request) -> Union[Any, RedirectResponse]:
    # redirect_uri = request.url_for("callback")
    return await app_oauth.authorize_redirect(request, "http://localhost:8000/callback")


# @app.get("/me")
# async def me(request: Request):
#     s = requests.Session()
#     s.headers.
#     print(response)


if __name__ == "__main__":
    uvicorn.run(app)

"""
