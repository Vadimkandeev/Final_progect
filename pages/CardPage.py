import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

class CardPage:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.data = DataProvider()
        url = ConfigProvider().get("ui", "base_url")

    @allure.step("Получить имя карточки:")
    def get_card_name(self) -> str:
        return self.__driver.find_element(By.CSS_SELECTOR, ".js-card-details").text


    @allure.step("Получить данные карточки ДО изменения информации:")
    def get_card_info_before_update(self) -> dict:
        data_before = {"name": "",
                       "description": ""}
        with allure.step("открыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-name").click()

        with allure.step("получить название карточки"):
            card_name = self.__driver.find_element(By.CSS_SELECTOR, '#js-dialog-title').get_property('textContent')
            data_before["name"] = card_name

        with allure.step("получить описание карточки"):
            card_description = self.__driver.find_element(By.CSS_SELECTOR, '.js-desc').text
            data_before["description"] = card_description

        data_before = {"name": card_name,
                       "description": card_description}
        
        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, '.js-close-window').click()

        return data_before

    
    @allure.step("Получить данные карточки ПОСЛЕ изменения информации:")
    def get_card_info_after_update(self) -> dict:
        with allure.step("открыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-details").click()

        with allure.step("получить название карточки"):
            card_name = self.__driver.find_element(By.CSS_SELECTOR, '#js-dialog-title').get_property('textContent')

        with allure.step("получить описание карточки"):
            card_description = self.__driver.find_element(By.CSS_SELECTOR, '.js-desc').text

        data_after = {"name": card_name,
                      "description": card_description}
        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, '.js-close-window').click()

        return data_after


    @allure.step("Изменить данные карточки:")
    def update_card(self, name: str, description: str):
        with allure.step("открыть карточку нажатием на неё"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-name").click()

        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.js-card-detail-title-input")))
        
        with allure.step("кликнуть название карточки"):
            self.__driver.find_element(By.CSS_SELECTOR, "textarea.js-card-detail-title-input").click()
        
        with allure.step("удалить старое название карточки"):
            self.__driver.find_element(By.CSS_SELECTOR, ".is-editing").clear()

        with allure.step("ввести новое название карточки"):
            self.__driver.find_element(By.CSS_SELECTOR, ".is-editing").send_keys(name)
            self.__driver.find_element(By.CSS_SELECTOR, ".is-editing").send_keys(Keys.ENTER)

        with allure.step("кликнуть в поле \"Описание\""):
            self.__driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Main content area, start typing to enter text."]').click()

        with allure.step("ввести новое описание в поле \"Описание\""):
            self.__driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Main content area, start typing to enter text."]').send_keys(description)

        with allure.step("нажать кнопку \"Сохранить\""):
            self.__driver.find_element(By.CSS_SELECTOR, 'input[value=Сохранить]:first-child').click()

        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Закрыть диалоговое окно"]').click()


    @allure.step("Удалить карточку:")
    def delete_card(self):
        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".js-card-menu")))

        with allure.step("нажать кнопку с иконкой \"карандаш\""):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-menu").click()

        with allure.step("нажать кнопку \"Архивировать\""):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-archive").click()


    @allure.step("Получить список, в котором находится открытая карточка:")
    def get_list_of_card(self) -> str:
        with allure.step("открыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-name").click()

        with allure.step("получить название списка, в котором находится карточка"):
            list_name = self.__driver.find_element(By.CSS_SELECTOR, ".js-open-move-from-header").text

        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, '.js-close-window').click()
            return list_name
        

    @allure.step("Получить название списка карточки ДО перемещения:")
    def get_card_list_before_moving(self) -> str:

        with allure.step("открыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-name").click()

        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.js-open-move-from-header')))
        
        with allure.step("получить название списка карточки"):
            list_name_before = self.__driver.find_element(By.CSS_SELECTOR, '.js-open-move-from-header').text

        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, '.js-close-window').click()

        return list_name_before

    
    @allure.step("Получить название списка карточки ПОСЛЕ перемещения:")
    def get_card_list_after_moving(self) -> str:
        with allure.step("открыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, ".js-card-name").click()

        with allure.step("получить название списка карточки"):
            list_name_after = self.__driver.find_element(By.CSS_SELECTOR, '.js-open-move-from-header').text

        with allure.step("закрыть карточку"):
            self.__driver.find_element(By.CSS_SELECTOR, '.js-close-window').click()

        return list_name_after