from typing import TypedDict, Optional
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

import time

class SonnikTypeArticle(TypedDict):
    title: str
    text : str

class SonnikTypeResponse(TypedDict):
    data: list[SonnikTypeArticle]
    error: str | None

class Sonnik:
    __time_to_wait: int = 2
    __count_result: int = 2
    __url: str = 'https://horo.mail.ru/sonnik/'
    __xpath_button: str = "//button[contains(@class, 'button') and contains(@class, 'button_nowrap') and contains(@class, 'button_color_project')]"
    __xpath_search_by_urls: str = "//div[contains(@class, 'newsitem') and contains(@class, 'newsitem_vertical') and contains(@class, 'newsitem_special') and contains(@class, 'newsitem_border_bottom') and contains(@class, 'js-pgng_item')]"
    __xpath_text: str = "//div[contains(@class, 'article__item') and contains(@class, 'article__item_alignment_left') and contains(@class, 'article__item_html')]" 

    def interpret(self, dream_text_image: str) -> SonnikTypeResponse:
        self.__dream_text_image: str = dream_text_image
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--headless')
        return self.__parsing_page(options_chrome)
        
    def __parsing_page(self, options) -> SonnikTypeResponse:
        data: list[SonnikTypeArticle] = []

        try:
            self.__browser = webdriver.Chrome(options=options) 
            self.__page_load(self.__url)
            self.__enter_text_image()
            self.__push_button()
            data: list[SonnikTypeArticle] = self.__get_data()
            self.__browser.quit()
        except Exception as ex:
            print(f'Упал класс Sonnik, ошибка: {ex}')
            return {"data": data, "error": f'Упал класс Sonnik, ошибка: {ex}'}

        else:
            return {"data": data, "error": None}

    def __page_load(self, url) -> None:
        self.__browser.get(url)

    def __enter_text_image(self) -> None:
        self.__browser.implicitly_wait(self.__time_to_wait)
        text_box: WebElement = self.__browser.find_element(By.CLASS_NAME, value="input__field")
        text_box.send_keys(self.__dream_text_image)

    def __push_button(self) -> None:
        self.__browser.implicitly_wait(self.__time_to_wait)
        button: WebElement = self.__browser.find_element(By.XPATH, self.__xpath_button) 
        button.click()

    def __get_data(self) -> list[SonnikTypeArticle]:
        data: list[SonnikTypeArticle] = []
        self.__browser.implicitly_wait(self.__time_to_wait)
        articles: list[dict[str, str]] | None = self.__get_article_urls()

        if articles == None:
            result: SonnikTypeArticle = self.__parsing_article()
            data.append(result)
            return data

        for article in articles:
            self.__page_load(article["url"])
            result: SonnikTypeArticle = self.__parsing_article()
            data.append(result)
            self.__browser.back()

        return data
    
    def __parsing_article(self) -> SonnikTypeArticle:
        title: str = self.__browser.find_element(By.TAG_NAME, "h1").text
        article_text: str = self.__browser.find_element(By.XPATH, self.__xpath_text).text

        article: SonnikTypeArticle = {
                "title": title,
                "text" : article_text,
                }
        return article

    def __get_article_urls(self) -> list[dict[str, str]] | None:
        links: list[dict[str, str]] = []
        self.__browser.implicitly_wait(self.__time_to_wait)
        elements: list[WebElement] = self.__browser.find_elements(By.XPATH, self.__xpath_search_by_urls )

        if elements != []:
            for element in elements[:self.__count_result]:
                result: str | None = self.__parsing_urls(element)
                if result == None:
                    continue
                links.append({'url': result})

        return None if links == [] else links

    def __parsing_urls(self, webElement) -> str | None:
        url: str | None =  webElement.find_element(By.TAG_NAME, "a").get_attribute('href')
        if url == None :
            return None
        return url

if '__main__' == __name__:
    sonnik = Sonnik()
    result = sonnik.interpret('лошадь')
    result = sonnik.interpret('лосось')
    result = sonnik.interpret(';sdlkf')
    print(result)
