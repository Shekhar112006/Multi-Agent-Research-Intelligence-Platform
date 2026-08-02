from app.modules.papers.processing.pdf_extractor import PDFExtractor

extractor = PDFExtractor()

result = extractor.extract(
    "storage/papers/62fe1de3-ee83-4371-bd12-ecdf424a8096.pdf"

)

print(result["pages"])
print(result["text"][:1000])