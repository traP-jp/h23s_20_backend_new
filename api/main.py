from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from api import crud, models, schemas
from api.database import SessionLocal, engine
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.requests_client import OAuth2Session
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Configurations
CLIENT_ID = "mh2QFGcvbMkHGNZD50ydorIaaMyABDh1c6Rn"
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8000/auth"
AUTHORIZE_URL = "https://q.trap.jp/api/v3/oauth2/authorize"
TOKEN_URL = "https://q.trap.jp/api/v3/oauth2/token"

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    SessionMiddleware, secret_key="secret-key", session_cookie="sessionid"
)


class TraqOAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware processing for certain paths
        if str(request.url.path) in ["/", "/auth"]:
            response = await call_next(request)
        else:
            # Retrieve token from cookie
            token = request.cookies.get("token")

            if token:
                # Use token to call traQ API
                client = OAuth2Session(CLIENT_ID, token=token)
                resp = client.get("https://q.trap.jp/api/v3/users/me")
                resp.raise_for_status()
                traq_id = resp.json().get("name")

                # Store traq_id in request.state
                request.state.traq_id = traq_id

                response = await call_next(request)
            else:
                # Raise HTTPException with 401 status code if token does not exist
                raise HTTPException(status_code=401, detail="Unauthorized")

        return response


app.add_middleware(TraqOAuthMiddleware)


client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope="read write")


@app.get("/auth")
async def auth(request: Request):
    uri, _ = client.create_authorization_url(AUTHORIZE_URL)
    return RedirectResponse(url=uri)


@app.get("/callback")
async def auth(request: Request, responce: Response):
    code = request.query_params.get("code")

    token = client.fetch_token(TOKEN_URL, "grant_type=authorization_code", code=code)
    print(token)

    # session に token を保存
    responce.set_cookie("token", token["access_token"])

    return {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


@app.get("/")
async def route():
    return "Hello"


@app.post("/points")
async def points(point: schemas.Point, db: Session = Depends(get_db)):
    crud.add_point(db, point, traq_id=traq_id)


@app.get("/ranking", response_model=List[schemas.User])
async def ranking(db: Session = Depends(get_db)):
    return crud.get_ranking(db)


@app.get("/me", response_model=schemas.User)
async def current_user(db: Session = Depends(get_db)):
    return crud.current_user(db, traq_id)


@app.put("/me")
async def update_user(user: schemas.User, db: Session = Depends(get_db)):
    return user
