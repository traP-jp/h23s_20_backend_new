""" 動きません（traQ OAuth）
import json
from typing import Any, Union
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from pydantic import BaseModel
import requests

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="19711f9f78d73ae2c7114f031bd13663eb5391e1aee816768411")

oauth = OAuth()
oauth.register(
    name="traq",
    client_id="bmLpJkCgkcPuQKedUIRpWFee7EE7zXSsIHpp",
    client_secret="HVoKtKIqp7tmnQ1YiTr0uK0PvzgnUKZsZHFn",
    access_token_url="https://q.trap.jp/api/v3/oauth2/token",
    access_token_params={
        "grant_type": "authorization_code"
    },
    authorize_url="https://q.trap.jp/api/v3/oauth2/authorize",
    authorize_params=None,
    api_base_url="https://q.trap.jp/api/v3",
    # client_kwargs={"timeout": Timeout(10.0)},
)

app_oauth = oauth.create_client("traq")

@app.get("/callback")
async def callback(request: Request):
    token = await app_oauth.authorize_access_token(request)

    obj = requests.Session()
    res = obj.request(
        'get',
        "https://q.trap.jp/api/v3/me",
        cookies={
            "session": token
        }
    )

    return res

@app.get("/login", response_model=None)
async def login(request: Request) -> Union[Any, RedirectResponse]:
    # redirect_uri = request.url_for("callback")
    return await app_oauth.authorize_redirect(request, "http://localhost:8000/callback")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
"""


from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "hello world!"}