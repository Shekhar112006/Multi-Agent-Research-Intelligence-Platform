from pydantic import BaseModel


class Methodology(BaseModel):
    research_type: str
    research_design: str
    participants: str
    sample_size: str
    data_collection: str
    tools_instruments: str
    analysis_method: str
    evaluation_metrics: list[str]
    limitations: list[str]


class MethodologyResponse(BaseModel):
    paper_id: str
    methodology: Methodology