from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from lexicon import PeriodZodiacButtons, ZodiacButtons, HoroCompatibility  

@dataclass
class ComparisonType:
    Female: ZodiacButtons 
    Male: ZodiacButtons 


class Horoscope:
    __instance = None
    __cache = {}
    __last_reset_time = "15.09.2023"

    def __new__(
        cls,
        zodiac: ZodiacButtons | None = None,
        period: PeriodZodiacButtons | None = None,
        comparison: ComparisonType | None = None,
    ):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        zodiac: ZodiacButtons | None = None,
        period: PeriodZodiacButtons | None = None,
        comparison: ComparisonType | None = None,
    ):
        self.zodiac = zodiac
        self.period = period
        self.comparison = (
            f"{comparison.Female.name}_{comparison.Male.name}"
            if comparison is not None
            else comparison
        )
        __ua = UserAgent()
        self.__headers = {
            "User-Agent": __ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    async def get_horo(self) -> dict[str, str]:
        self.__reset_cache()
        key_cache = f"{self.zodiac}_{self.period}"
        if key_cache in self.__cache:
            return self.__cache[key_cache]
        text = await self.__get_horo_text()
        assert text
        self.__cache[key_cache] = text
        return text

    async def get_compare(self):
        self.__reset_cache()
        key_cache = f"{self.comparison}"
        if key_cache in self.__cache:
            return self.__cache[key_cache]

        return await self.__get_compare_text()

    async def __get_horo_text(self) -> dict[str, str]:
        response = {}
        assert self.zodiac
        assert self.period
        link = f"https://horo.mail.ru/prediction/{self.zodiac.name}/{self.period.name}/"
        response_result = await self.__get_page(link=link)
        beautifulsoup: BeautifulSoup = BeautifulSoup(
            markup=response_result, features="lxml"
        )
        text = beautifulsoup.find("main", {"itemprop": "articleBody"})
        title = beautifulsoup.find("h1", {"data-qa": "Title"})
        rating_list = beautifulsoup.find_all("ul", class_="b5ce145b7d")

        assert text
        assert title
        response["text"] = text.text
        response["title"] = title.text
        response["finance"] = rating_list[0]["aria-label"]
        response["health"] = rating_list[1]["aria-label"]
        response["love"] = rating_list[2]["aria-label"]
        return response

    async def __get_compare_text(self) -> dict[str, str]:
        assert self.comparison
        link = f"https://horo.mail.ru/compatibility/zodiac/{HoroCompatibility[self.comparison].value}/"
        response_result = await self.__get_page(link=link)
        beautifulsoup: BeautifulSoup = BeautifulSoup(
            markup=response_result, features="lxml"
        )
        text = beautifulsoup.find(
            "div", 
            class_="c1cd057491"
        )
        
        title = beautifulsoup.find("h1", class_="c30ebf5669 abf242312f ef123d1686")
        assert text 
        assert title 
        formatted_text = re.sub(r'(\d+\.\s[^:]+:\s*[А-ЯЁ][а-яё]+)', r'\n\n<b>\1</b>\n', text.text)
        return {
            "title": title.text,
            "text": formatted_text.strip()
        }

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
