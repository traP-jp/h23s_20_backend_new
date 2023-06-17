from fastapi import Depends, FastAPI, HTTPException, status
from api import crud, models, schemas
from api.database import SessionLocal, engine
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

traq_id = "1"

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
async def current_user(db: Session = Depends(get_db), traq_id: str = traq_id):
    return crud.current_user(db, traq_id)

# @app.put("/me")
# async def update_user(user = schemas.User, db: Session = Depends(get_db)):
#     pass