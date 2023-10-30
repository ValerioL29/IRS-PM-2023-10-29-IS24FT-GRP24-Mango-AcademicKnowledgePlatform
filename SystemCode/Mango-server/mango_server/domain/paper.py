from pydantic import BaseModel


class Paper(BaseModel):
    id: str
    title: str
    authors: dict
    abstract: str | None
    code: str | None
    s2_url: str | None
    pwc_url: str | None
    tldr: str | None
    field_of_study: str | None
    venue: str | None
    external_ids: dict | None


class PaperProfile(BaseModel):
    id: str
    date: str
    trend: float
    likes: int
    saves: int
    reads: int
    shares: int


class PaperInDB(BaseModel):
    id: str
    paper_data: dict
    vector: list[float]
