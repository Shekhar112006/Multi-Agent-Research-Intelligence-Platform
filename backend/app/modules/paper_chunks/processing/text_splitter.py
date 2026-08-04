"""
Simple text splitter.
"""


class TextSplitter:
    """
    Splits long text into chunks.
    """

    def split(
        self,
        text: str,
        chunk_size: int = 1000,
    ) -> list[str]:
        """
        Split text into chunks.
        """

        paragraphs = text.split("\n\n")

        chunks = []

        current_chunk = ""

        for paragraph in paragraphs:

            if len(current_chunk) + len(paragraph) <= chunk_size:

                current_chunk += paragraph + "\n\n"

            else:

                if current_chunk.strip():

                    chunks.append(current_chunk.strip())

                current_chunk = paragraph + "\n\n"

        if current_chunk.strip():

            chunks.append(current_chunk.strip())

        return chunks