from pydantic import BaseModel


class PaperComparison(BaseModel):
    paper_id: str
    title: str

    methodology: str
    claims: list[str]

    datasets: list[str]
    evaluation_metrics: list[str]
    results: list[str]
    limitations: list[str]


class ComparisonAnalysis(BaseModel):
    common_methods: list[str]
    method_differences: list[str]

    dataset_differences: list[str]

    performance_differences: list[str]

    common_limitations: list[str]

    research_opportunities: list[str]


class ComparisonResponse(BaseModel):
    project_id: str
    papers: list[PaperComparison]
    analysis: ComparisonAnalysis
