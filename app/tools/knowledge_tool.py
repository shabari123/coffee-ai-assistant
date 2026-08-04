from app.config import KNOWLEDGE_SEARCH_RESULTS
from app.knowledge.embedding import EmbeddingService
from app.knowledge.vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)

embedding_service = EmbeddingService()
vector_store = VectorStore()


def search_knowledge(question: str):
    """
    Search the Swasthya Coffee knowledge base.

    Use this tool when the user asks about:
    - coffee brewing
    - coffee storage
    - coffee origins
    - blogs
    - FAQs
    - shipping policy
    - refund policy
    - general coffee knowledge

    Do NOT use this tool for product catalog searches or order status.
    """
    logger.info("Knowledge search: %s", question)
    embedding = embedding_service.embed(question)

    result = vector_store.search(
        embedding=embedding,
        n_results=KNOWLEDGE_SEARCH_RESULTS,
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    return {
        "documents": documents,
        "sources": metadatas,
    }