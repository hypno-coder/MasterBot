from datetime import datetime, timedelta, timezone

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Horoscope:
    __instance = None
    __cache = {}
    __last_reset_time = "15.09.2023"

    def __new__(cls, zodiac: str, period: str):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, zodiac: str, period: str):
        self.zodiac = zodiac
        self.period = period 
        __ua = UserAgent()
        self.__headers = {
            "User-Agent": __ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    async def get(self) -> dict[str, str | None]:
        self.__reset_cache()
        key_cache = f"{self.zodiac}_{self.period}"
        if key_cache in self.__cache:
            return self.__cache[key_cache]
        text = await self.__get_text()
        assert text
        self.__cache[key_cache] = text
        return text

    async def __get_text(self) -> dict[str, str | None]:
        response = {}
        link = f"https://horo.mail.ru/prediction/{self.zodiac}/{self.period}/"
        response_result = await self.__get_page(link=link)
        beautifulsoup: BeautifulSoup = BeautifulSoup(
            markup=response_result, features="lxml"
        )
        text = beautifulsoup.find("section", {'data-qa': 'Article'})
        title = beautifulsoup.find("h1", {'data-qa': 'Title'})
        assert text
        assert title 
        response["text"] = text.text 
        response["title"] = title.text
        return response 

    async def __get_page(self, link):
        async with httpx.AsyncClient(
            headers=self.__headers, follow_redirects=True
        ) as htx:
            result: httpx.Response = await htx.get(url=link)
            if result.status_code != 200:
                return await self.__get_page(link)
            else:
                return await result.aread()

    def __reset_cache(self):
        current_date = datetime.now(timezone(timedelta(hours=3))).strftime("%d.%m.%Y")
        if datetime.strptime(current_date, "%d.%m.%Y") > datetime.strptime(
            self.__last_reset_time, "%d.%m.%Y"
        ):
            self.__cache = {}
            self.__last_reset_time = current_date
