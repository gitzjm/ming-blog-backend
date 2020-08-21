"""
文章相关Schema
"""
from pydantic import BaseModel


class ArticleBaseSchema(BaseModel):
    """文章Schema基类"""
    title: str
    body: str


class Article(ArticleBaseSchema):
    """文章"""
    ...
