from api import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy import desc

# ポイントを受け取って更新 (POST \points)
def add_point(db: Session, point: schemas.Point, traq_id: str):
    t = point.point_type
    if t == 'low':
        point = 1
    elif t == 'middle':
        point = 3
    elif t == 'high':
        point = 5
    # else:
        # エラーハンドリング
    
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    user.total_point += point  # User テーブルに point sum を持っておく必要がありそう
    db.commit()

# total_point 降順に User を取得. (GET \ranking)
def get_ranking(db: Session, limit: int = 10):
    res = db.query(models.User).order_by(desc(models.User.total_point)).limit(limit).all()
    return res

def current_user(db: Session, traq_id: str):
    return db.query(models.User).filter(models.User.traq_id == traq_id).first()

def update_user(db: Session, user_update: schemas.User):
    user = db.query(models.User).filter(models.User.traq_id == user_update.traq_id).first()
    # for文とかでまとめられたらいいのに
    if user_update.github_id:
        user.github_id = user_update.github_id
    if user_update.atcoder_id:
        user.atcoder_id = user_update.atcoder_id
    if user_update.traq_point_type:
        user.traq_point_type = user_update.traq_point_type
    if user_update.github_point_type:
        user.github_point_type = user_update.github_point_type
    if user_update.atcoder_point_type:
        user.atcoder_point_type = user_update.atcoder_point_type
    db.commit()
    return user