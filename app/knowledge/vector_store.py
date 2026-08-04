import chromadb

from app.config import CHROMA_COLLECTION_NAME, VECTOR_DB_PATH

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(CHROMA_COLLECTION_NAME)

    def add_documents(self, ids, documents, embeddings, metadatas) -> None:
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, embedding, n_results=5):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

    def clear(self) -> None:
        try:
            self.client.delete_collection(CHROMA_COLLECTION_NAME)
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            CHROMA_COLLECTION_NAME
        )