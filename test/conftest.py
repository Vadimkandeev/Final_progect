import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.BoardApi import BoardApi
from configuration.ConfigProvider import ConfigProvider

# base_url = "https://trello.com/1/"
token = "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):

        timeout = ConfigProvider().getint("ui", "timeout")

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser


    with allure.step("Закрыть браузер"):
        browser.quit()

@pytest.fixture
def api_client() -> BoardApi:
    #url = ConfigProvider().get("api", "base_url")
    return BoardApi(ConfigProvider().get("api", "base_url"), token)  


@pytest.fixture
def api_client_no_auth() -> BoardApi:
    return BoardApi(ConfigProvider().get("api", "base_url"), "")  


@pytest.fixture
def dummy_board_id() -> str:
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)

    with allure.step("Pre create a board"):
        resp = api.create_board("board_for_deleted").get("id")
    
    return resp


@pytest.fixture
def delete_board() -> str:
    dictionary = {"board_id": ""}
    print("board_id", dictionary) 
    yield dictionary
    
    with allure.step("Delete a board after test"):
        api = BoardApi(ConfigProvider().get("api", "base_url"), token)
        api.delete_board_by_id(dictionary.get("board_id"))
   

# @pytest.fixture
# def create_list():
#     api = BoardApi(ConfigProvider().get("api", "base_url"), token)

#     with allure.step("Pre create a board"):
#         resp = api.create_board("board_for_deleted").get("id")
 