import httpx
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Sonnik:
    __max_length = 4000

    def __init__(self, key_word):
        self.__base_link = f'https://horo.mail.ru/sonnik/search/?q={key_word}&b=0&clb11934144='
        self.__ua = UserAgent()
        self.__headers = {
                "User-Agent": self.__ua.random, 
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    async def get(self) -> list[dict[str, str]] | None:
        downloaded_page = await self.__download_page(self.__base_link)
        if downloaded_page == None:
            return
        links = self.__create_link_list(downloaded_page)
        articles = await self.__get_article_list(links[:3])
        return articles 

    async def __download_page(self, link, timeout=10, max_retries=3) -> bytes | None:
        for _ in range(max_retries):
            try:
                async with httpx.AsyncClient(headers=self.__headers, follow_redirects=True, timeout=timeout) as htx:
                    result: httpx.Response = await htx.get(url=link)
                    result.raise_for_status()
                    return await result.aread()
            except httpx.ReadTimeout:
                continue
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error occurred: {exc}")
                break
        return None 

    def __create_link_list(self, page) -> list[str]:
        soup: BeautifulSoup = BeautifulSoup(markup=page, features='lxml')
        elements = soup.find_all(name='a', class_='link-holder')
        links = [item.get('href') for item in elements if item.get('href') is not None]
        return links

    async def __get_article_list(self, links) -> list[dict[str, str]] | None:
        articles: list[dict[str, str]] = []
        for link in links:
            page = await self.__download_page(f'https://horo.mail.ru{link}')
            article = self.__get_article(page)
            if article == None:
                return
            articles.append(article)

        return None if len(articles) == 0 else articles

    def __get_article(self, page) -> dict[str, str] | None:
        soup: BeautifulSoup = BeautifulSoup(markup=page, features='lxml')
        header = soup.find(name='h1', class_='hdr__inner')
        paragraph = soup.find(name='div', class_='article__item')
        if header == None or paragraph == None:
            return
        return {'header': header.text, 'paragraph': self.__truncate_text(paragraph.text) }

    def __truncate_text(self, text) -> str:
        if len(text) <= self.__max_length:
            return text
        sentences: str = text.split('.')
        truncated_text: str = ''
        for sentence in sentences:
            if len(truncated_text) + len(sentence) +1 <= self.__max_length:
                truncated_text += sentence + '.'
            else:
                break
        return truncated_text
