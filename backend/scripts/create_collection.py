from app.modules.embeddings.vector_db.qdrant_service import QdrantService


def main():
    qdrant = QdrantService()

    qdrant.create_collection("paper_chunks")

    print(">>> paper_chunks collection ready")


if __name__ == "__main__":
    main()
