import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver


    def get_boards_before_add_board(self) -> int:
        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.board-tile-details-name")))

        with allure.step("посчитать количество досок"):
            fields = self.__driver.find_elements(By.CSS_SELECTOR, "div.board-tile-details-name")

            return len(fields)


    def get_boards_after_add_board(self) -> int:
        with allure.step("нажать кнопку \"Рабочее простанство Trello\" и перейти в Рабочее простанство Trello"):
            self.__driver.find_element(By.XPATH, '//p[text()="Рабочее пространство Trello"]').click()

        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.board-tile-details-name")))

        with allure.step("посчитать количество досок"):
            fields = self.__driver.find_elements(By.CSS_SELECTOR, "div.board-tile-details-name")

            return len(fields)
        

    def get_boards_before_delete(self) -> int:
        with allure.step("подождать загрузки всех необходимых элементов"):
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[title="New board"]')))

        with allure.step("посчитать количество досок"):
            fields = self.__driver.find_elements(By.CSS_SELECTOR, "div.board-tile-details-name")

            return len(fields)


    def get_boards_after_delete(self) -> int:
        with allure.step("посчитать количество досок"):
            fields = self.__driver.find_elements(By.CSS_SELECTOR, "div.board-tile-details-name")

            return len(fields)


    @allure.step("Создать доску {board_name}:")
    def create_board_ui(self, board_name: str) -> None:
        with allure.step("нажать кнопку \"Создать доску\""):
            self.__driver.find_element(By.CSS_SELECTOR, "li[data-testid=create-board-tile]").click()

        with allure.step("ввести название доски в поле \"Заголовок доски\""):
            self.__driver.find_element(By.CSS_SELECTOR, "input[data-testid=create-board-title-input]").send_keys(board_name)

        with allure.step("подождать, когда кнопка \"Создать\" станет кликабельной"):
            WebDriverWait(self.__driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="create-board-submit-button"]')))

        with allure.step("нажать кнопку \"Создать\""):
            self.__driver.find_element(By.CSS_SELECTOR, 'button[data-testid="create-board-submit-button"]').click()


    @allure.step("Открыть доску")
    def open_board(self):
        self.__driver.find_element(By.CSS_SELECTOR, 'div[title="New board"]').click()
