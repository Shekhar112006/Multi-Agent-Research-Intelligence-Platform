from app.modules.retrieval.schemas.retrieval_result import RetrievalResult


class ContextBuilder:
    """
    Converts retrieval results into structured LLM context.
    """

    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:

        context_parts: list[str] = []

        for result in results:
            context_parts.append(
                f"""Paper ID: {result.paper_id}
Project ID: {result.project_id}
Chunk: {result.chunk_index}
Score: {result.score:.4f}

{result.text}"""
            )

        return "\n\n---\n\n".join(context_parts)