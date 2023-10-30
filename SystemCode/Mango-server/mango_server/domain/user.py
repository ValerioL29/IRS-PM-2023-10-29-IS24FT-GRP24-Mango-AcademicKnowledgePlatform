from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    organization: str
    interested_fields: list[str]


class Bookmark(BaseModel):
    id: str
    user_id: str
    title: str
    paper_ids: list[str]


class UserQuery(BaseModel):
    user_id: str
    role: str
    organization: str
    interested_fields_0: str
    interested_fields_1: str
    date: int
    time: int
