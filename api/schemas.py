from pydantic import BaseModel
from typing import Optional, List


class Point(BaseModel):
    point_type: str


class User(BaseModel):
    traq_id: str
    github_id: Optional[str]
    atcoder_id: Optional[str]
    traq_point_type: Optional[str]
    github_point_type: Optional[str]
    atcoder_point_type: Optional[str]
    total_point: int = 0
    github_total_contributions: int = 0
    traq_total_posts: int = 0
    atcoder_total_ac: int = 0

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    github_id: Optional[str]
    atcoder_id: Optional[str]
    traq_point_type: Optional[str]
    github_point_type: Optional[str]
    atcoder_point_type: Optional[str]

    class Config:
        orm_mode = True


class Leaf(BaseModel):
    position_x: int
    position_y: int
    color: str
    size: str

    class Config:
        orm_mode = True


class Tree(BaseModel):
    branch_count: int
    leaves: List[Leaf]

    class Config:
        orm_mode = True


class Trees(BaseModel):
    total_point: int
    trees: List[Tree]

    class Config:
        orm_mode = True
