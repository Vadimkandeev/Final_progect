import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

class ListPage:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.data = DataProvider()
        url = ConfigProvider().get("ui", "base_url")

    def get_cards_on_list(self):
        cards = self.__driver.find_elements(By.CSS_SELECTOR, ".js-card-details")
        return cards


    @allure.step("Создать карточку")
    def create_card(self, name: str):
        with allure.step("нажать кнопку \"Добавить карточку\""):
            self.__driver.find_element(By.XPATH, '//div[@id="board"]/div[1]/div[last()]//*[text()="Добавить карточку"]').click()

        with allure.step("в поле \"Ввести заголовок для этой карточки\" ввести название карточки"):
            self.__driver.find_element(By.CSS_SELECTOR, "textarea[placeholder=\"Ввести заголовок для этой карточки\"]").send_keys(name)

        with allure.step("нажать клавишу Enter"):
            self.__driver.find_element(By.CSS_SELECTOR, "textarea[placeholder=\"Ввести заголовок для этой карточки\"]").send_keys(Keys.ENTER)


    @allure.step("Перенести карточку в другую колонку:")
    def move_card(self):
        with allure.step("найти карточку, которую надо перенести в другую колонку"):
            draggable = self.__driver.find_element(By.XPATH, '//span[text()="New card"]')

        with allure.step("найти колонку, в которую надо перенести карточку"):
            droppable = self.__driver.find_element(By.XPATH, '//textarea[text()="Second list"]')

        with allure.step("взять карточку и перенести её в нужную колонку"):
            ActionChains(self.__driver).drag_and_drop(draggable, droppable).perform()    
        