from app.modules.paper_chunks.processing.text_splitter import (
    TextSplitter,
)

from app.modules.papers.processing.pdf_extractor import (
    PDFExtractor,
)

extractor = PDFExtractor()

result = extractor.extract(
    "storage/papers/62fe1de3-ee83-4371-bd12-ecdf424a8096.pdf"
)

pages = result["pages"]
text = result["text"]
splitter = TextSplitter()

chunks = splitter.split(text)

print(f"Pages : {pages}")
print(f"Chunks: {len(chunks)}")

print()

print(chunks[0][:500])