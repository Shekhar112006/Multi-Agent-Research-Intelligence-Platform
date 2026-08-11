"""
Builds context from retrieved paper chunks.
"""


class ContextBuilder:
    """
    Converts retrieved chunks into LLM-ready context.
    """

    def build(self, results) -> str:
        """
        Build a context string from Qdrant search results.
        """

        context_parts = []

        for result in results:
            payload = result.payload

            context_parts.append(
                f"""
Paper ID: {payload["paper_id"]}
Chunk: {payload["chunk_index"]}

{payload["text"]}
"""
            )

        return "\n\n---\n\n".join(context_parts)