from app.models.document import Document


class TextChunker:

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, documents: list[Document]) -> list[Document]:
        chunks = []
        for document in documents:
            text = document.content
            start = 0

            while start < len(text):
                end = start + self.chunk_size
                chunk_text = text[start:end]
                chunks.append(
                    Document(
                        title=document.title,
                        url=document.url,
                        content=chunk_text,
                    )
                )
                start += self.chunk_size - self.chunk_overlap
        return chunks