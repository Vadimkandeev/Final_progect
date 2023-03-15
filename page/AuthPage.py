from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AuthPage: 

    def __init__(self, driver:WebDriver) -> None:
        self.__url="https://trello.com/login"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)

    def login_as(self,email:str, password:str):
        self.__driver.find_element(By.CSS_SELECTOR, "#user").send_keys(email)
        self.__driver.find_element(By.CSS_SELECTOR, "#login").click()
 
        # Дожидаемся, отрисовки поля Пароля
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='presentation']")))

        self.__driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        self.__driver.find_element(By.CSS_SELECTOR, "#login-submit").click()

    
  



