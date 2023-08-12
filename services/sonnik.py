from typing import TypedDict
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class SonnikTypeArticle(TypedDict):
    title: str
    text : str


class SonnikTypeResponse(TypedDict):
    data: list[SonnikTypeArticle]
    error: str | None


class Sonnik:
    __response_data: list[SonnikTypeArticle] = []
    __time_to_wait: int = 2
    __count_result: int = 2
    __max_length: int = 4000
    __url: str = 'https://horo.mail.ru/sonnik/'
    __xpath_button: str = "//button[contains(@class, 'button') and contains(@class, 'button_nowrap') and contains(@class, 'button_color_project')]"
    __xpath_search_by_urls: str = "//div[contains(@class, 'newsitem') and contains(@class, 'newsitem_vertical') and contains(@class, 'newsitem_special') and contains(@class, 'newsitem_border_bottom') and contains(@class, 'js-pgng_item')]"
    __xpath_text: str = "//div[contains(@class, 'article__item') and contains(@class, 'article__item_alignment_left') and contains(@class, 'article__item_html')]" 

    def interpret(self, dream_text_image: str) -> SonnikTypeResponse:
        self.__dream_text_image: str = dream_text_image
        return self.__parsing_page()
        
    def __parsing_page(self) -> SonnikTypeResponse:

        try:            
            urls: list[dict[str, str]] | None = self.__get_article_urls()
            pool = Pool(processes=len(urls))
            pool.map(self.__get_data, urls)
        except Exception as ex:
            print(f'Упал класс Sonnik, ошибка: {ex}')
            return {"data": self.__response_data, "error": f'Упал класс Sonnik, ошибка: {ex}'}

        else:
            return {"data": self.__response_data, "error": None}

    def __page_load(self, url, browser) -> None:
        browser.get(url)

    def __enter_text_image(self, browser) -> None:
        browser.implicitly_wait(self.__time_to_wait)
        text_box: WebElement = browser.find_element(By.CLASS_NAME, value="input__field")
        text_box.send_keys(self.__dream_text_image)

    def __push_button(self, browser) -> None:
        browser.implicitly_wait(self.__time_to_wait)
        button: WebElement = browser.find_element(By.XPATH, self.__xpath_button) 
        button.click()

    def __get_data(self, url) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options) 

        if url == None:
            result: SonnikTypeArticle = self.__parsing_article(browser)
            self.__response_data.append(result)
            return

        self.__page_load(url, browser)
        result: SonnikTypeArticle = self.__parsing_article(browser)
        self.__response_data.append(result)

        browser.quit()
    
    def __parsing_article(self, browser) -> SonnikTypeArticle:
        title: str = browser.find_element(By.TAG_NAME, "h1").text
        article_text: str = browser.find_element(By.XPATH, self.__xpath_text).text

        article: SonnikTypeArticle = {
                "title": title,
                "text" : self.__truncate_text(article_text),
                }
        return article

    def __truncate_text(self, text) -> str:
        if len(text) <= self.__max_length:
            return text
    
        sentences: str = text.split('.')
        truncated_text: str = ''

        for sentence in sentences:
            if len(truncated_text) + len(sentence) + 1 <= self.__max_length:
                truncated_text += sentence + '.'
            else:
                break
        
        return truncated_text


    def __get_article_urls(self) -> list:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        browser = webdriver.Chrome(options=options) 
        self.__page_load(self.__url, browser)
        self.__enter_text_image(browser)
        self.__push_button(browser)

        links: list = []
        browser.implicitly_wait(self.__time_to_wait)
        elements: list[WebElement] = browser.find_elements(By.XPATH, self.__xpath_search_by_urls )

        if elements != []:
            for element in elements[:self.__count_result]:
                result: str | None = self.__parsing_urls(element)
                if result == None:
                    continue
                links.append(result)
        
        browser.quit()
        return [None] * self.__count_result if links == [] else links

    def __parsing_urls(self, webElement) -> str | None:
        url: str | None =  webElement.find_element(By.TAG_NAME, "a").get_attribute('href')
        return url

if __name__ == "__main__":
    sonnik = Sonnik()
    result = sonnik.interpret('лошадь')
    print(result)
