import requests

from app.models.document import Document
from app.config import WEBSITE_URL
from app.knowledge.html_cleaner import HtmlCleaner


class WebsiteLoader:

    def load_pages(self) -> list[Document]:
        response = requests.get(
            f"{WEBSITE_URL}/wp-json/wp/v2/pages",
            timeout=10
        )

        response.raise_for_status()

        pages = response.json()

        documents = []

        for page in pages:
            documents.append(
                Document(
                    title=page["title"]["rendered"],
                    url=page["link"],
                    content=HtmlCleaner.clean(page["content"]["rendered"]),
                )
            )

        return documents