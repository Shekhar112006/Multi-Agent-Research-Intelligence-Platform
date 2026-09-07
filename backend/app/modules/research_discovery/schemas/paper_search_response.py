from pydantic import BaseModel


class Author(BaseModel):
    authorId: str | None = None
    name: str | None = None


class OpenAccessPdf(BaseModel):
    url: str | None = None
    status: str | None = None


class PaperSearchResult(BaseModel):
    paperId: str
    title: str
    abstract: str | None = None
    authors: list[Author] = []
    year: int | None = None
    citationCount: int = 0
    url: str | None = None
    openAccessPdf: OpenAccessPdf | None = None


class PaperSearchResponse(BaseModel):
    query: str
    total: int
    papers: list[PaperSearchResult]