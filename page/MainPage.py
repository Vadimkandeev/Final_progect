from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class MainPage:

    def __init__(self, driver:WebDriver) -> None:
        self.__driver = driver
    
    def get_current_url(self) -> str:
        return self.__driver.current_url
    
    def open_menu(self) -> str:
        self.__driver.find_element(By.CSS_SELECTOR, "button[data-testid='header-member-menu-button']").click()

    def get_account_info(self) -> list[str]:
        container = self.__driver.find_element(By.CSS_SELECTOR, "div[data-testid='account-menu']>div>div:last-child")     

        fields = container.find_elements(By.CSS_SELECTOR, "div")
        name = fields[0].text
        email = fields[1].text

        return [name, email]
