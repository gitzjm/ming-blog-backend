from fastapi import Body
from pydantic import BaseModel


class ArticleBaseSchema(BaseModel):
    title: str
    body: str


class Article(ArticleBaseSchema):
    ...
