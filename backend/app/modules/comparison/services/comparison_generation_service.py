"""
Service for AI-powered research paper comparison.
"""

import json

from app.modules.generation.services.generation_service import (
    GenerationService,
)


class ComparisonGenerationService:
    """
    Generates structured comparisons between research papers.
    """

    def __init__(
        self,
        generation_service: GenerationService | None = None,
    ):
        self.generation_service = (
            generation_service
            if generation_service is not None
            else GenerationService()
        )

    def compare(
        self,
        comparison_data: list[dict],
    ) -> dict:
        """
        Compare multiple research papers using the LLM.
        """

        context_parts = []

        for paper in comparison_data:
            context_parts.append(
                f"""
PAPER ID:
{paper["paper_id"]}

TITLE:
{paper["title"]}

CONTENT:
{paper["text"]}
"""
            )

        context = "\n".join(context_parts)

        question = """
Compare the provided research papers.

Extract and return ONLY valid JSON using this structure:

{
    "papers": [
        {
            "paper_id": "string",
            "title": "string",
            "methodology": "string",
            "claims": [],
            "datasets": [],
            "evaluation_metrics": [],
            "results": [],
            "limitations": []
        }
    ],
    "analysis": {
        "common_methods": [],
        "method_differences": [],
        "dataset_differences": [],
        "performance_differences": [],
        "common_limitations": [],
        "research_opportunities": []
    }
}

Rules:

1. Use ONLY information present in the provided papers.
2. Do not invent datasets, metrics, results, or claims.
3. Keep claims grounded in the paper content.
4. If information is unavailable, use an empty list or "Not available".
5. Compare the papers rather than summarizing them independently.
"""

        response = self.generation_service.generate(
            question=question,
            context=context,
            response_format={
                "type": "object",
            },
        )

        return json.loads(response)



