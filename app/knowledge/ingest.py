from app.knowledge.loader import WebsiteLoader
from app.knowledge.chunker import TextChunker
from app.knowledge.embedding import EmbeddingService
from app.knowledge.vector_store import VectorStore


class KnowledgeIngestionService:

    def __init__(self):
        self.loader = WebsiteLoader()
        self.chunker = TextChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def ingest(self):
        print("Clearing existing knowledge...")
        self.vector_store.clear()

        print("Loading documents...")
        documents = self.loader.load_pages()
        print(f"Loaded {len(documents)} documents")

        print("Chunking documents...")
        chunks = self.chunker.chunk(documents)
        print(f"Created {len(chunks)} chunks")

        ids = []
        embeddings = []
        texts = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            print(f"Embedding chunk {index + 1}/{len(chunks)}")
            embedding = self.embedding_service.embed(chunk.content)
            ids.append(str(index))
            texts.append(chunk.content)
            embeddings.append(embedding)

            metadatas.append({
                "title": chunk.title,
                "url": chunk.url,
            })

        print("Saving to Vector DB...")

        self.vector_store.add_documents(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print("Knowledge ingestion completed.")