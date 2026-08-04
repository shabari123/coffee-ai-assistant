from bs4 import BeautifulSoup


class HtmlCleaner:

    @staticmethod
    def clean(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        return text