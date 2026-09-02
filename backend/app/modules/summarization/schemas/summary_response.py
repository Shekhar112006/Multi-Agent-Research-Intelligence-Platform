from pydantic import BaseModel


class SummaryResponse(BaseModel):
    paper_id: str
    summary: str