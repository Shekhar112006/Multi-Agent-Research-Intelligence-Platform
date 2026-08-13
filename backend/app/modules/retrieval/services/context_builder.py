"""
Builds LLM-ready context from retrieved chunks.
"""

from app.modules.retrieval.schemas.retrieval_result import RetrievalResult


class ContextBuilder:
    """
    Converts retrieved chunks into a single context string
    suitable for an LLM prompt.
    """

    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:

        context_parts = []

        for result in results:
            context_parts.append(
                f"""
Paper ID: {result.paper_id}
Chunk: {result.chunk_index}

{result.text}
""".strip()
            )

        return "\n\n---\n\n".join(context_parts)