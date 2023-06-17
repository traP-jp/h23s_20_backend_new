from pydantic import BaseModel
from typing import Optional

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