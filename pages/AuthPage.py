import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configuration.ConfigProvider import ConfigProvider



class AuthPage: 

    def __init__(self, driver:WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url=url+"/login"
        self.__driver = driver

    @allure.step("Открыть страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Авторизоваться под пользователем {email}: {password}")
    def login_as(self, email: str, password: str):
        with allure.step("В поле \"Укажите адрес электронной почты\" ввести email"):
            self.__driver.find_element(By.CSS_SELECTOR, "#user").send_keys(email)
        with allure.step("Нажать кнопку \"Продолжить\""):
            self.__driver.find_element(By.CSS_SELECTOR, "#login").click()

        with allure.step("Подождать полной загрузки поля \"Введите пароль\" (отображения иконки с глазом)"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[role=presentation]")))

        with allure.step("В поле \"Введите пароль\" ввести пароль"):
            self.__driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        with allure.step("Нажать кнопку \"Войти\""):
            self.__driver.find_element(By.CSS_SELECTOR, "#login-submit").click()

  



