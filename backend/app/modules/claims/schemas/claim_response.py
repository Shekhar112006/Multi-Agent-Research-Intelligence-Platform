from pydantic import BaseModel


class Claim(BaseModel):
    claim: str
    evidence: str
    type: str
    importance: str


class ClaimResponse(BaseModel):
    paper_id: str
    claims: list[Claim]