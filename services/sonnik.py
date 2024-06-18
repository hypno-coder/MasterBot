import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from fake_useragent import UserAgent

from lexicon import letterComparator


class Sonnik:
    __max_length = 4000

    def __init__(self, key_word):
        self.key_word = key_word
        self.__base_link = (
            f"https://horo.mail.ru/sonnik/{self.__get_first_letter(key_word)}/"
        )
        self.__ua = UserAgent()
        self.__headers = {
            "User-Agent": self.__ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    async def get(self) -> list[dict[str, str]] | None:
        try:
            downloaded_page = await self.__download_page(self.__base_link)
            if downloaded_page == None: return
            link = self.__get_article_link(downloaded_page)
            downloaded_article = await self.__download_page(link)
            if downloaded_article == None: return
            article = self.__get_article(downloaded_article)
        except Exception:
            return
        return article

    async def __download_page(self, link, timeout=10, max_retries=3) -> bytes | None:
        for _ in range(max_retries):
            try:
                async with httpx.AsyncClient(
                    headers=self.__headers, follow_redirects=True, timeout=timeout
                ) as htx:
                    result: httpx.Response = await htx.get(url=link)
                    result.raise_for_status()
                    return await result.aread()
            except httpx.ReadTimeout:
                continue
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error occurred: {exc}")
                break
        return None

    def __get_article_link(self, page) -> str | None:
        soup: BeautifulSoup = BeautifulSoup(markup=page, features="lxml")
        element = soup.find(name="ul", class_="d5a33e6558")
        if element == None or not isinstance(element, (Tag)):
            return
        for li in element.find_all("li"):
            a_tag = li.find("a")
            if a_tag and a_tag.text.lower() == self.key_word:
                return a_tag["href"]
        return

    def __get_article(self, page) -> list[dict[str, str]] | None:
        soup: BeautifulSoup = BeautifulSoup(markup=page, features="lxml")
        section = soup.find("section", attrs={"data-qa": "Article"})
        if section == None or not isinstance(section, (Tag)):
            return
        header = self.__get_header(section)
        main = self.__get_main(section)
        if header == None or main == None:
            return
        return [header, *main]

    def __get_main(self, section) -> list[dict[str, str]] | None:
        articles = []
        main = section.find("main", {"itemprop": "articleBody"})
        if main == None or not isinstance(main, (Tag)):
            return
        article_items = main.find_all("div", {"article-item-type": "html"})
        if article_items == None:
            return
        for item in article_items[:-1]:
            h2 = item.find("h2")
            p = item.find("p")
            articles.append(
                {
                    "title": h2.get_text() if h2 != None else "_",
                    "paragraph": p.get_text() if p != None else "_",
                }
            )
        return articles

    def __get_header(self, section) -> dict[str, str] | None:
        header = section.find("header", class_="e22e8f9371")
        if header == None or not isinstance(header, (Tag)):
            return
        title_element = header.find("h1", {"data-qa": "Title"})
        paragraph_element = header.find("div", class_="f344ddc593")
        if title_element == None or paragraph_element == None:
            return
        title = title_element.get_text()
        paragraph = paragraph_element.get_text()

        return {
            "title": title,
            "paragraph": self.__truncate_text(paragraph),
        }

    def __truncate_text(self, text: str) -> str:
        if len(text) <= self.__max_length:
            return text
        sentences: list[str] = text.split(".")
        truncated_text: str = ""
        for sentence in sentences:
            if len(truncated_text) + len(sentence) + 1 <= self.__max_length:
                truncated_text += sentence + "."
            else:
                break
        return truncated_text

    def __get_first_letter(self, key_word: str):
        first_letter = key_word[0].lower()
        return letterComparator[first_letter]
