from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response, UploadFile, File
from api import crud, models, schemas
from api.database import SessionLocal, engine
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from authlib.integrations.requests_client import OAuth2Session
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from os import getenv

import json
import base64


# Configurations
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
REDIRECT_URI = getenv("REDIRECT_URI")
AUTHORIZATION_URL = getenv("AUTHORIZATION_URL")
TOKEN_URL = getenv("TOKEN_URL")
USER_API_URL = getenv("USER_API_URL")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope="read write")


class TraqOAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware processing for certain paths
        if str(request.url.path) in [
            "/",
            "/ping",
            "/docs",
            "/openapi.json",
            "/callback",
            "/auth",
        ]:
            response = await call_next(request)
            return response

        # Retrieve token from cookie
        token = request.session.get("token")

        if not token:
            return Response(status_code=401)

        client = OAuth2Session(CLIENT_ID, token=token)
        resp = client.get(USER_API_URL)
        resp.raise_for_status()
        traq_id = resp.json().get("name")

        # Store traq_id in request.state
        request.state.traq_id = traq_id

        response = await call_next(request)

        return response


app.add_middleware(TraqOAuthMiddleware)

app.add_middleware(
    SessionMiddleware, secret_key="secret-key", session_cookie="sessionid"
)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def route():
    return {"message": "pong"}


@app.get("/test")
async def test_traq_id(request: Request):
    traq_id = request.state.traq_id
    return {"traq_id": traq_id}


@app.get("/auth")
async def auth(request: Request):
    uri, _ = client.create_authorization_url(AUTHORIZATION_URL)
    return RedirectResponse(url=uri)


@app.get("/callback")
async def auth(request: Request, responce: Response):
    code = request.query_params.get("code")
    token = client.fetch_token(TOKEN_URL, "grant_type=authorization_code", code=code)

    # session に token を保存
    request.session["token"] = token

    return {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


@app.get("/users", response_model=List[str])
async def users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


@app.get("/{user_id}/trees", response_model=schemas.Trees)
async def trees(request: Request, db: Session = Depends(get_db), user_id):
    # ここに木のまわりの処理
    
    # 進捗確認
    traq_id = request.state.traq_id
    user = db.query(schemas.User).filter(schemas.User.traq_id == traq_id).first()
    diff_github = crud.get_progress_github(db, traq_id)
    if diff_github:
        crud.add_point(db, user.github_point_type, traq_id)
    diff_traq = crud.get_progress_traq(db, traq_id)
    if diff_traq:
        crud.add_point(db, user.traq_point_type, traq_id)
    diff_atcoder = crud.get_progress_atcoder(db, traq_id)
    if diff_atcoder:
        crud.add_point(db, user.atcoder_point_type, traq_id)


@app.post("/points")
async def points(request: Request, point: schemas.Point, db: Session = Depends(get_db)):
    traq_id = request.state.traq_id
    crud.add_point(db, point.point_type, traq_id=traq_id)


@app.get("/ranking", response_model=List[schemas.User])
async def ranking(db: Session = Depends(get_db)):
    return crud.get_ranking(db)


@app.get("/me", response_model=schemas.User)
async def get_user(request: Request, db: Session = Depends(get_db)):
    traq_id = request.state.traq_id
    return crud.get_user(db, traq_id)


@app.put("/me", response_model=schemas.User)
async def update_user(
    request: Request, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    traq_id = request.state.traq_id
    return crud.update_user(db, traq_id, user)


# @app.get("/temp")
# async def temp(request: Request, db: Session = Depends(get_db)):
#     traq_id = request.state.traq_id
#     token = request.session.get("token")
#     res = crud.get_progress_traq(db, token["access_token"], traq_id)
#     return res


@app.post("./image")
async def image(request: Request, db: Session = Depends(get_db), file: bytes = File(...)):
    traq_id = request.state.traq_id
    img_binary = base64.b64decode(file)
    img_png = np.frombuffer(img_binary, dtype=np.uint8)
    img = cv2.imdecode(img_png, cv2.IMREAD_COLOR)
    image_file = f"api/images/{traq_id}.png"
    cv2.imwrite(image_file, img)

# /{user_id}/trees が呼ばれた時に発火するように修正

"""
@app.get("/triggers/github")
async def check_github(request: Request, db: Session = Depends(get_db)):
    traq_id = request.state.traq_id
    flag, point_type = crud.get_progress_github(db, traq_id)
    return flag


@app.get("/triggers/atcoder")
async def check_atcoder(request: Request, db: Session = Depends(get_db)):
    traq_id = request.state.traq_id
    flag, point_type = crud.get_progress_atcoder(db, traq_id)
    return flag
"""
