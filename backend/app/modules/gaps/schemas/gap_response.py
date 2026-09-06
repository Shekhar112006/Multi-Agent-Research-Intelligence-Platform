from pydantic import BaseModel


class ResearchGap(BaseModel):
    gap: str
    evidence: str
    type: str
    importance: str


class GapResponse(BaseModel):
    paper_id: str
    gaps: list[ResearchGap]