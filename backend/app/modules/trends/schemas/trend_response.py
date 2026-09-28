"""
Response schemas for research trend analysis.
"""

from pydantic import BaseModel


class ResearchTrend(BaseModel):
    """
    Represents a research trend identified across multiple papers.
    """

    topic: str
    description: str
    evidence: str
    supporting_papers: list[str]
    direction: str
    confidence: str


class TrendResponse(BaseModel):
    """
    Response returned after trend analysis.
    """

    project_id: str
    trends: list[ResearchTrend]
