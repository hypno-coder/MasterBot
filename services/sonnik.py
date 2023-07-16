from typing import TypedDict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class SonnikTypeArticle(TypedDict):
    title: str
    type : str
    text : str

class SonnikTypeResponse(TypedDict):
    data: list[SonnikTypeArticle]
    error: bool

class Sonnik:
    def __init__(self):
        self.__time_to_wait: int = 2
        self.__count_result = 2
        self.__is_error = False
        self.__url: str = 'https://horo.mail.ru/sonnik/'
        self.__xpath_button: str = "//button[contains(@class, 'button') and contains(@class, 'button_nowrap') and contains(@class, 'button_color_project')]"
        self.__xpath_search_by_urls: str = "//div[contains(@class, 'newsitem') and contains(@class, 'newsitem_vertical') and contains(@class, 'newsitem_special') and contains(@class, 'newsitem_border_bottom') and contains(@class, 'js-pgng_item')]"
        self.__xpath_text: str = "//div[contains(@class, 'article__item') and contains(@class, 'article__item_alignment_left') and contains(@class, 'article__item_html')]" 

    def interpret(self, dream_text_image: str) -> SonnikTypeResponse:
        self.__dream_text_image: str = dream_text_image
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--headless')
        return self.__page_parsing(options_chrome)
        
    def __page_parsing(self, options) -> SonnikTypeResponse:
        data = []
        current_downloads: int = 0 
        max_download_count: int = 2

        while True:
            try:
               self.__browser = webdriver.Chrome(options=options) 
               self.__page_load(self.__url)
               self.__enter_text_image()
               self.__push_button()
               data: list[SonnikTypeArticle] = self.__get_data()
            except Exception as ex:
                if current_downloads < max_download_count:
                    current_downloads += 1
                    self.__browser.quit()
                    continue
                else:
                    print(f"Ошибка парсинга \n {ex}")
                    self.__is_error = True
                    self.__browser.quit()
                    return {"data": data, "error": self.__is_error}
            else:
                self.__browser.quit()
                return {"data": data, "error": self.__is_error}

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
        result: list[SonnikTypeArticle] = []
        self.__browser.implicitly_wait(self.__time_to_wait)
        articles: list[dict[str, str]] = self.__get_article_urls()
        for article in articles:
            self.__page_load(article["url"])
            title: str = self.__browser.find_element(By.TAG_NAME, "h1").text
            article_text: str = self.__browser.find_element(By.XPATH, self.__xpath_text).text
            data: SonnikTypeArticle = {
                    "type" : article["type"],
                    "title": title,
                    "text" : article_text,
                    }
            result.append(data)
            self.__browser.back()

        return result

    def __get_article_urls(self) -> list[dict[str, str]]:
        links: list[dict[str, str]] = []
        self.__browser.implicitly_wait(self.__time_to_wait)
        elements: list[WebElement] = self.__browser.find_elements(By.XPATH, self.__xpath_search_by_urls )
        for element in elements[:self.__count_result]:
            url: str | None = element.find_element(By.TAG_NAME, "a").get_attribute('href')
            type: str | None = element.find_element(By.CLASS_NAME, "newsitem__param").text
            if isinstance(url, str):
                data: dict = {"url": url, "type": type}
                links.append(data)
            else:
                print('Парсинг не смог собрать ссылки')

        return links 


if '__main__' == __name__:
    sonnik = Sonnik()
    sonnik.interpret('Лошадь')
