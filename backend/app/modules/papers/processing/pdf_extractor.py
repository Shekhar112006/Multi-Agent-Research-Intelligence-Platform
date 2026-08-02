"""
PDF text extraction service.
"""

import fitz


class PDFExtractor:
    """
    Extracts text from PDF documents.
    """

    def extract(
        self,
        pdf_path: str,
    ) -> dict:
        """
        Extract all text from a PDF.

        Returns:
            {
                "pages": int,
                "text": str,
            }
        """

        document = fitz.open(pdf_path)

        text = []

        for page in document:
            text.append(page.get_text())

        document.close()

        return {
            "pages": len(text),
            "text": "\n".join(text),
        }