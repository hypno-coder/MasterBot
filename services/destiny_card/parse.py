import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from errors import send_error_message

from .types import DestinyCardClientType


class DestinyCard:

    def __init__(self, user: DestinyCardClientType):
        self.__base_link = f"https://gadalkindom.ru/matritsa-sudby?m_name={user['name']}&gender={user['gender']}&m_date={user['date']}"
        self.__ua = UserAgent()
        self.__headers = {
            "User-Agent": self.__ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    @classmethod
    async def get(cls, user: DestinyCardClientType):
        obj: DestinyCard = cls(user)
        return await obj.__launch()

    async def __launch(self):
        try:
            downloaded_page = await self.__download_page(self.__base_link)
            filtered_results = self.__page_filtering(downloaded_page)
            return filtered_results
        except Exception as e:
            await send_error_message(e)
            raise e

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
                raise ValueError("Не загружается страница для парсинга Карты Судьбы")
        return None

    def __page_filtering(self, page):
        try:
            soup = BeautifulSoup(markup=page, features="lxml")
            soup = self.__remove_parents_of_article(soup)
            soup = self.__remove_tag_before(soup)
            soup = self.__remove_tag_after(soup)
            soup = self.__remove_tag_with_current_class(soup, "autor-blok")
            soup = self.__add_syle(soup)
        except Exception as e:
            raise ValueError(
                "Не получается обработать загруженную страницу Карты Судьбы"
            )
        else:
            return soup.prettify()

    def __remove_parents_of_article(self, soup):
        return soup.article.extract()

    def __remove_tag_before(self, soup):
        for tag in soup.find_all():
            if tag.name == "h3":
                return soup
            tag.decompose()
        return soup

    def __remove_tag_after(self, soup):
        tag = soup.find("h3", string="Расшифровка чакровой карты здоровья")
        if tag:
            siblings = tag.find_next_siblings()
            for sibling in siblings:
                sibling.decompose()
            tag.find_previous_sibling().decompose()
            tag.decompose()
        return soup

    def __remove_tag_with_current_class(self, soup, clc):
        tags_to_remove = soup.find_all("div", class_=clc)
        for tag in tags_to_remove:
            tag.decompose()
        return soup

    def __add_syle(self, soup):
        soup["style"] = "font-size: 20px"
        return soup
