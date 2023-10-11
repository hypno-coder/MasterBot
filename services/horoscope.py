import httpx
from datetime import datetime, timezone, timedelta
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Horoscope:
    __instance = None
    __cache = {}
    __last_reset_time = '15.09.2023' 

    def __new__(cls, zodiac: str):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, zodiac: str):
        self.zodiac = zodiac
        __ua = UserAgent()
        self.__headers = {
                "User-Agent": __ua.random, 
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    async def get(self) -> str | None:
        self.reset_cache()
        if self.zodiac in self.__cache: 
            return self.__cache[self.zodiac]
        text = await self.__get_text()
        if text == None:
            return
        self.__cache[self.zodiac] = text
        return text 

    async def __get_text(self) -> str | None: 
        link = f'https://horo.mail.ru/prediction/{self.zodiac}/today/' 
        response_result = await self.__get_page(link=link)
        beautifulsoup: BeautifulSoup = BeautifulSoup(markup=response_result, features='lxml')
        text = beautifulsoup.find(name='div', class_='article__text')
        if text == None: 
            return

        return text.text

    async def __get_page(self, link): 
        async with httpx.AsyncClient(headers=self.__headers, follow_redirects=True) as htx:
            result: httpx.Response = await htx.get(url=link)
            if result.status_code != 200:
                return await self.__get_page(link)
            else:
                return await result.aread()

    def reset_cache(self):
        current_date = datetime.now(timezone(timedelta(hours=3))).strftime("%d.%m.%Y")
        if datetime.strptime(current_date, "%d.%m.%Y") > datetime.strptime(self.__last_reset_time, "%d.%m.%Y"):
            self.__cache = {}
            self.__last_reset_time = current_date 
