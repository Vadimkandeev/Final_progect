import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.BoardApi import BoardApi

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.implicitly_wait(4)
        browser.maximize_window()
        yield browser


    with allure.step("Закрыть браузер"):
        browser.quit()

@pytest.fixture
def api_client() -> BoardApi:
    return BoardApi("https://trello.com/1/", "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxt\
                    iaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09")  


@pytest.fixture
def api_client_no_auth() -> BoardApi:
    return BoardApi("https://trello.com/1/", "")  


@pytest.fixture
def dummy_board_id() -> str:
    api = BoardApi("https://trello.com/1/", "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxt\
                    iaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09")
    resp = api.create_board("board_for_deleted").get("id")
    return resp


@pytest.fixture
def delete_board() -> str:
    dictionary = {"board_id": ""}
    yield dictionary

    api = BoardApi("https://trello.com/1/", "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxt\
                    iaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09")
    api.delete_board_by_id(dictionary.get("board_id"))
    

