from pydantic import BaseModel

class Point(BaseModel):
    point_type: str

class User(BaseModel):
    traq_id: str = ""
    github_id: str = ""
    atcoder_id: str = ""
    traq_point_type: str = ""
    github_point_type: str = ""
    atcoder_point_type: str = ""
    total_point: int = 0