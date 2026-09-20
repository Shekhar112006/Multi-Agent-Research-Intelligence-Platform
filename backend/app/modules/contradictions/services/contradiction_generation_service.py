"""
Service for AI-powered contradiction detection.
"""

import json

from app.modules.generation.services.generation_service import (
    GenerationService,
)


class ContradictionGenerationService:
    """
    Uses the LLM to determine whether matched claims contradict each other.
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

    def analyze(
        self,
        matches: list[dict],
    ) -> list[dict]:
        """
        Analyze potentially related claim pairs for contradictions.
        """

        if not matches:
            return []

        context_parts = []

        for index, match in enumerate(matches, start=1):
            claim_a = match["claim_a"]
            claim_b = match["claim_b"]

            context_parts.append(
                f"""
MATCH {index}

PAPER A CLAIM:
{claim_a["claim"]}

PAPER A EVIDENCE:
{claim_a.get("evidence", "")}

PAPER B CLAIM:
{claim_b["claim"]}

PAPER B EVIDENCE:
{claim_b.get("evidence", "")}

SEMANTIC SIMILARITY:
{match["similarity"]}
"""
            )

        context = "\n".join(context_parts)

        question = """
Analyze the potentially related research claims below.

Determine whether the claims actually contradict each other.

Return ONLY valid JSON using this structure:

{
    "contradictions": [
        {
            "claim_a": "string",
            "evidence_a": "string",
            "claim_b": "string",
            "evidence_b": "string",
            "contradiction_type": "string",
            "explanation": "string",
            "confidence": "high"
        }
    ]
}

Rules:

1. Only identify genuine contradictions.
2. Semantic similarity alone does NOT mean contradiction.
3. Do not treat different wording as contradiction.
4. Do not invent information.
5. Use only the claims and evidence provided.
6. If the claims are compatible, do not include them.
7. contradiction_type should describe the contradiction, such as:
   - result
   - conclusion
   - methodology
   - finding
   - interpretation
8. confidence must be one of:
   - high
   - medium
   - low
9. Keep explanations concise.
"""

        response = self.generation_service.generate(
            question=question,
            context=context,
            response_format={"type": "object"},
        ).strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        result = json.loads(response)

        if isinstance(result, dict):
            contradictions = result.get("contradictions", [])

            if isinstance(contradictions, list):
                return contradictions

        return []