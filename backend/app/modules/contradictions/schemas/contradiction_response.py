"""
Response schemas for research contradiction detection.
"""

from pydantic import BaseModel


class Contradiction(BaseModel):
    """
    Represents a contradiction identified between two research papers.
    """

    paper_a_id: str
    paper_b_id: str

    claim_a: str
    evidence_a: str

    claim_b: str
    evidence_b: str

    contradiction_type: str
    explanation: str
    confidence: str


class ContradictionResponse(BaseModel):
    """
    Response returned after contradiction analysis.
    """

    project_id: str
    contradictions: list[Contradiction]