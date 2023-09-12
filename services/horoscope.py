import httpx
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

async def get_response(link: str): 
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as htx:
        result: httpx.Response = await htx.get(url=link)
        if result.status_code != 200:
            return await get_response(link=link)
        else:
            return await result.aread()


async def get_text_horoscope(zodiac: str):
    link = f'https://horo.mail.ru/prediction/{zodiac}/today/' 
    response_result = await get_response(link=link)
    beautifulsoup: BeautifulSoup = BeautifulSoup(markup=response_result, features='lxml')
    text = beautifulsoup.find(name='div', class_='article__text')
    if text == None:
        return
    
    return text.text 
