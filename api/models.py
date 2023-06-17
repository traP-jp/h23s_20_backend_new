from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from api.database import Base


class User(Base):
    __tablename__ = "users"
    traq_id = Column(String(255), primary_key=True)
    total_point = Column(Integer, default=0)
    github_id = Column(String(255))
    atcoder_id = Column(String(255))
    traq_point_type = Column(String(255))
    github_point_type = Column(String(255))
    atcoder_point_type = Column(String(255))
    github_total_contributions = Column(Integer, default=0)
    traq_total_posts = Column(Integer, default=0)
    atcoder_total_ac = Column(Integer, default=0)

    class Config:
        orm_mode = True


class Tree(Base):
    __tablename__ = "trees"
    tree_id = Column(Integer, primary_key=True)
    traq_id = Column(String(255), ForeignKey("users.traq_id"))
    branch_count = Column(Integer)

    class Config:
        orm_mode = True


class Leaf(Base):
    __tablename__ = "leaves"
    tree_id = Column(Integer, ForeignKey("trees.tree_id"), primary_key=True)
    leaf_id = Column(Integer, primary_key=True)
    position_x = Column(Integer)
    position_y = Column(Integer)
    color = Column(String(255))
    size = Column(String(255))

    class Config:
        orm_mode = True
