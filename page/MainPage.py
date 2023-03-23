import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configuration.ConfigProvider import ConfigProvider


class MainPage:

    def __init__(self, driver:WebDriver) -> None:
        self.__driver = driver
        self.url = ConfigProvider().getint("ui", "base_url")
        self.__url = self.url+"u/vadimkandeev_1975/boards"


    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    
    @allure.step("Получить текущий  URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url
    
    @allure.step("Открыть боковое меню")
    def open_menu(self) -> str:
        self.__driver.find_element(By.CSS_SELECTOR, "button[data-testid='header-member-menu-button']").click()

    @allure.step("Прочитать информацию о пользователе")
    def get_account_info(self) -> list[str]:
        container = self.__driver.find_element(By.CSS_SELECTOR, "div[data-testid='account-menu']>div>div:last-child")     
        fields = container.find_elements(By.CSS_SELECTOR, "div")
        name = fields[0].text
        email = fields[1].text

        return [name, email]
    
    @allure.step("Добавить куки авторизации")
    def add_cookie(self):
        cookie = {
            "name": "tiken",
            "value": "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"
        }
        self.__driver.add_cookie(cookie)

    @allure.step("Нажать кнопку Создать в шапке")
    def open_create_form(self):
        self.__driver.find_element(By.CSS_SELECTOR, "button[data-testid=header-create-menu-button]").click()


    @allure.step("Выбрать {number} элемент в списке")
    def choose_option(self, number=1):
        popover = self.__driver.find_element(By.CSS_SELECTOR, "section[data-testid=header-create-menu-popover]")
        lis = popover.find_element(By.CSS_SELECTOR, "li")
        lis[number-1].click()

    @allure.step("Указать имя новой доски = {board_name}")
    def fill_name(self, board_name:str):
        self.__driver.find_element(By.CSS_SELECTOR, "input[data-testid=create-board-title-input]").send_keys(board_name)
 

    @allure.step("Нажать сохранить")
    def click_save_button(self):
        self.__driver.find_element(By.CSS_SELECTOR, "button[data-testid=create-board-submit-button]").click()
        WebDriverWait(self.__driver, 10).until(EC.url_contains(self.url, ""))