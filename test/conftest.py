import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.BoardApi import BoardApi
from configuration.ConfigProvider import ConfigProvider
from faker import Faker
fake = Faker()

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

    yield dictionary
    
    with allure.step("Удалить доску после теста"):
        api = BoardApi(ConfigProvider().get("api", "base_url"), token)
        api.delete_board_by_id(dictionary.get("board_id"))


# ----------------------- Здесь я буду пистаь новые фикстуры -----------------------------------

@pytest.fixture
def get_id_list(dummy_board_id):
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    
    with allure.step("Получить id первого списка"):
        list_id_1 = api.get_list(dummy_board_id)[0]["id"] # Получить айди первого списка
    with allure.step("Получить id следующего списка"):
        list_id_2 = api.get_list(dummy_board_id)[1]["id"] # Получить айди следующего списка    
    with allure.step("Возвращаем  id списков"):
        
        return list_id_1, list_id_2, dummy_board_id


@pytest.fixture
def create_new_card(get_id_list):
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    id_board = get_id_list[2]
    with allure.step("Получить id листа"):
        id_list = get_id_list[0]
    with allure.step("Создание карточки на листе"):
        card = api.add_card(id_list, fake.text(20)) # Создать карточку на листе

    with allure.step("Получить id карточки"):
        id_card = card["id"]
    
    return  id_card, id_list, id_board




# ----------------------- Это окончание моих экспериментов -----------------------------------
 
     

