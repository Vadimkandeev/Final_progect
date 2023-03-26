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

"""
@pytest.fixture
def delete_board() -> str:
    dictionary = {"board_id": ""}
     # print("board_id", dictionary) 
    yield dictionary
    
    with allure.step("Удалить доску после теста"):
        api = BoardApi(ConfigProvider().get("api", "base_url"), token)
        api.delete_board_by_id(dictionary.get("board_id"))

"""
# ----------------------- Здесь я буду пистаь новые фикстуры на -----------------------------------
#------------  СОздание/Удаление доски
# ------------ ПОлучение айди списков
# ------------ Создание карточки
@pytest.fixture
def create_delete_a_board() -> str:
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    with allure.step("Создать Доску"):
        id_board = api.create_board("This is board from API test").get("id")
    yield id_board
    
    with allure.step("Удалить Доску"):
        api.delete_board_by_id(id_board)


@pytest.fixture
def get_id_list() -> str:
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    with allure.step("Получить список"):
        list_lists = api.get_list(create_delete_a_board) # Получить список
    with allure.step("Получить id первого списка"):
        list_id_1 = api.get_list(create_delete_a_board)[0]["id"] # Получить айди первого списка
    with allure.step("Получить id следующего списка"):
        list_id_2 = api.get_list(create_delete_a_board)[1]["id"] # Получить айди следующего списка    
    with allure.step("Возвращаем  id списков"):
        return list_id_1, list_id_2, 

@pytest.fixture
def create_new_card():
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    with allure.step("Создание карточки на листе"):
            id_list = get_id_list[0]
            id_card = api.add_card(id_list, fake.text(20)) # Создать карточку на листе

    return  id_card, id_list




# ----------------------- Это окончание моих экспериментов -----------------------------------
   
"""
@pytest.fixture
def get_list_from_a_board():
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)
    
    with allure.step("Создать доску перед тестом"):
        board_id = api.create_board("board_for_add_card").get("id")
        list_id = api.get_list(board_id)[0]["id"]

        card_id = api.add_card(list_id, fake.text(20))

        # print("RESP    ", board_id)
        # print("LIST_ID    ", list_id)
        # print("NAME++++++   ", card_id["name"])
        # print("ID++++++   ", card_id["id"]) 
        # print("RESP++++++   ", card_id)    
    return list_id, board_id


@pytest.fixture
def get_card_from_list():
    api = BoardApi(ConfigProvider().get("api", "base_url"), token)

    with allure.step("Создание доски с атрибутами"):
        with allure.step("Создание новой доски"):
            board = api.create_board("board_for_add_card")# Создать новую доску
        with allure.step("Получить id доски"):
            board_id = board.get("id") # Получить АЙДИ доски
        with allure.step("Получить список"):
            list_lists = api.get_list(board_id) # Получить список
        with allure.step("Получить id первого списка"):
            list_id = api.get_list(board_id)[0]["id"] # Получить айди первого списка
        with allure.step("Получить id следующего списка"):
            list_new_id = api.get_list(board_id)[1]["id"] # Получить айди следующего списка    
        with allure.step("Создание карточки на листе"):
            resp = api.add_card(list_id, fake.text(20)) # Создать карточку на листе
        with allure.step("Получить id карточки"):
            card_id = resp["id"] # Получить АЙДИ карточки
        with allure.step("Получить имя карточки"):
            card_name = resp["name"] # Получить имя карточки

        # print("RESP******", resp)
        # print("BOARD_ID******", board_id)
        # print("LIST_ID******", list_id)
        # print("CARD_ID******", card_id)
        # print("CARD_NAME******", card_name)
        # print("BOARD******", board)
        # print("list_lists******", list_lists)
        # print("LEN__list_lists******", len(list_lists))

        # print("List[][][][][][][][][]", list_lists[0]["id"])
        # print("List[][][][][][][][][]", list_lists[1]["id"])
                         
    return card_id, card_name, board_id, list_id, list_new_id

"""

