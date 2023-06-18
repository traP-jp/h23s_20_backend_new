from api import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc
from api.config import GITHUB_API_KEY, github_query, github_headers
import requests
import json


def get_all_users(db: Session) -> list[str]:
    users = db.query(models.User).all()
    return [user.traq_id for user in users]


def create_user(db: Session, traq_id: str):
    # user
    db_user = models.User(traq_id=traq_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # tree
    """
    db_tree = models.Tree(branch_count=0, traq_id=traq_id)
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    """


# 木を取得
def get_tree(db: Session, traq_id: str):
    # join で tree と leaf を取得
    trees = (
        db.query(models.Tree)
        .join(models.Leaf, models.Tree.tree_id == models.Leaf.tree_id)
        .filter(models.Tree.traq_id == traq_id)
        .all()
    )

    # 木の数だけループ
    res = []
    for tree in trees:
        # 木の情報を格納
        tree_res = {"branch_count": tree.branch_count, "leaves": []}
        # leaf の数だけループ
        for leaf in tree.leaves:
            # leaf の情報を格納
            leaf_res = {
                "position_x": leaf.position_x,
                "position_y": leaf.position_y,
                "color": leaf.color,
                "size": leaf.size,
            }
            # leaf を追加
            tree_res["leaves"].append(leaf_res)
        # tree を追加
        res.append(tree_res)
    return res


def insert_tree(db: Session, tree: schemas.Tree, traq_id: str):
    # tree を追加
    db_tree = models.Tree(branch_count=tree.branch_count, traq_id=traq_id)
    db.add(db_tree)
    db.commit()

    # leaf を追加
    for leaf in tree.leaves:
        db_leaf = models.Leaf(
            position_x=leaf.position_x,
            position_y=leaf.position_y,
            color=leaf.color,
            size=leaf.size,
            tree_id=db_tree.tree_id,
        )
        db.add(db_leaf)
    db.commit()

    return db_tree


# ポイントを受け取って更新 (POST \points)
def add_point(db: Session, point: str, traq_id: str) -> int:
    t = point.point_type
    if t == "low":
        point = 1
    elif t == "middle":
        point = 3
    elif t == "high":
        point = 5
    # else:
    # エラーハンドリング

    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    user.total_point += point  # User テーブルに point sum を持っておく必要がありそう
    total_point = user.total_point
    db.commit()

    print(total_point)


# total_point 降順に User を取得. (GET \ranking)
def get_ranking(db: Session, limit: int = 10):
    res = (
        db.query(models.User).order_by(desc(models.User.total_point)).limit(limit).all()
    )
    return res


def get_user(db: Session, traq_id: str):
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    # 暫定処置
    if user is None:
        db_user = models.User(
            traq_id=traq_id,
            total_point=0,
            github_total_contributions=0,
            traq_total_posts=0,
            atcoder_total_ac=0,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user = db.query(models.User).filter(models.User.traq_id == traq_id).first()

    print(user)
    return user


def update_user(db: Session, traq_id: str, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()

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

    db.refresh(user)
    return user



def get_progress_github(db: Session, traq_id: str):
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    point_type = user.github_point_type

    variables = {"userName": "SakanoYuito"}
    res = requests.post(
        "https://api.github.com/graphql",
        json={"query": github_query, "variables": variables},
        headers=github_headers,
    )

    contribution_total = json.loads(res.content)["data"]["user"][
        "contributionsCollection"
    ]["contributionCalendar"]["totalContributions"]

    diff = 0
    if user.github_total_contributions < contribution_total:
        diff = contribution_total - user.github_total_contributions
        user.github_total_contributions = contribution_total
        db.commit()
        return diff
    else:
        return diff


def get_progress_atcoder(db: Session, traq_id: str):
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    point_type = user.atcoder_point_type

    ac_count = 0
    res = requests.get(
        f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user.atcoder_id}&from_second=1687018869"
    )
    d = json.loads(res.content)
    for e in d:
        # print(e)
        if e["result"] == "AC":
            ac_count += 1

    diff = 0
    if user.atcoder_total_ac < ac_count:
        diff = ac_count - user.atcoder_total_ac
        user.atcoder_total_ac = ac_count
        db.commit()
        return diff
    else:
        return diff


traq_channels = [
    "b70ef91c-8fda-4124-a7e5-4648e18da6c5", # random/progress
    "9e822ec2-634e-4b9c-af30-41707f537426", # t/Algorithm/
    "7dc7d0e1-a7b9-4294-ba3e-1149a4c42c71", # t/CTF/
    "cde0fe1b-f225-415a-b302-0c7a7ab754e2", # t/Game
    "858ae414-21ec-40d8-be6a-012620db8edf", # t/graphics/
    "8d878ff5-f34f-43ab-8a0f-6a6f8f3202a3", # t/g/progressNSFW
    "8bd9e07a-2c6a-49e6-9961-4f88e83b4918", # t/sound/
    "112446e4-a8b5-4618-9813-75f08377ccc5"  # t/SysAd/
]

def get_progress_traq(db: Session, token: str, traq_id: str):
    header = {"Authorization": f"Bearer {token}"}
    user = db.query(models.User).filter(models.User.traq_id == traq_id).first()
    point_type = user.traq_point_type

    traq_uuid = json.loads(requests.get('https://q.trap.jp/api/v3/users/me', headers=header).content)["id"]
    posts = 0
    for channel in traq_channels:
        posts += json.loads(requests.get(f'https://q.trap.jp/api/v3/messages?after=2023-04-16T15%3A04%3A05Z&in={channel}&from={traq_uuid}&sort=-createdAt', headers=header).content)["totalHits"]
        print(posts)
    
    diff = 0
    if user.traq_total_posts < posts:
        diff = posts - user.traq_total_posts
        user.traq_total_posts = posts
        db.commit()
    return diff
