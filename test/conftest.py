import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from user_data.UserProvider import UserProvider
from testdata.DataProvider import DataProvider
from configuration.ConfigProvider import ConfigProvider

from pages.MainPage import MainPage
from pages.BoardPage import BoardPage
from pages.ListPage import ListPage
from pages.CardPage import CardPage
from pages.ApiPage import ApiForUI

from api.BoardAPI import BoardAPI
from api.CardAPI import CardAPI

@pytest.fixture
def test_data() -> DataProvider:
    with allure.step("Получить тестовые данные"):
        return DataProvider()
    

@pytest.fixture
def user_data() -> UserProvider:
    with allure.step("Получить данные пользователя"):
        return UserProvider()
    

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        timeout = ConfigProvider().get("ui", "timeout")
        browser_name = ConfigProvider().get("ui", "browser_name")
        base_url = ConfigProvider().get("ui", "base_url")
        url_for_token = ConfigProvider().get("ui", "url_for_token")
        token = UserProvider().get("user", "token")

        if browser_name == "chrome":
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        else:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        browser.implicitly_wait(timeout)
        browser.maximize_window()

        browser.get(base_url)

        browser.add_cookie({'name': 'token', 'value': token})
            
        browser.get(url_for_token)    

        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture
def api_client_for_ui() -> ApiForUI:
    with allure.step("Создать экземпляр класса ApiForUI"):
        return ApiForUI(
            ConfigProvider().get_api_url(),
            UserProvider().get_user_token())
 

@pytest.fixture
def for_delete_board(browser, test_data: dict, api_client_for_ui: ApiForUI):
    board_name = test_data.get("board_name")
    api_client_for_ui.create_board(board_name)

    yield browser


@pytest.fixture
def for_create_board(test_data: dict, api_client_for_ui: ApiForUI):
    org_id =test_data.get("org_id")
    board_name = test_data.get("board_name")

    yield

    board_list = api_client_for_ui.get_all_boards_by_org_id(org_id)
    length = len(board_list)
    count = 0
    for count in range(0, length):
        if board_list[count]["name"] == board_name:
            api_client_for_ui.delete_board_by_id(board_list[count]["id"])
            count = count + 1


@pytest.fixture
def dummy_board_for_ui(browser, test_data: dict, api_client_for_ui: ApiForUI):
    board_name = test_data.get("board_name")
    list_name = test_data.get("list_names")[0]

    resp = api_client_for_ui.create_board(board_name).get("id")

    board_page = BoardPage(browser)
    board_page.create_list_ui(list_name) 

    yield browser

    with allure.step("Удалить доску после теста"):
        api_client_for_ui.delete_board_by_id(resp)  


@pytest.fixture
def lists_name_on_board_for_ui(api_client_for_ui: ApiForUI, dummy_board_for_ui: str) -> dict:   
    lists_on_board = api_client_for_ui.get_lists_by_board_id(dummy_board_for_ui)

    with allure.step("получить названия колонок на доске"):    
        lists = {
            'list_one_id': lists_on_board[0]["name"],
            'list_two_id': lists_on_board[1]["name"],
            'list_three_id': lists_on_board[2]["name"]
        }

    with allure.step("перейти к удалению доски"): # удаление доски - после yield, тут написано, чтобы красиво было в отчёте
        yield lists


@pytest.fixture
def card_to_delete(browser, dummy_board_for_ui: str, test_data: dict):
    card_name = test_data.get("card_name")
    list_page = ListPage(browser)
    list_page.create_card(card_name)

@pytest.fixture
def dummy_board_for_moving(browser, test_data: dict, api_client_for_ui: ApiForUI): 
    board_name = test_data.get("board_name")
    list_names = test_data.get("list_names")
    card_name = test_data.get("card_name")

    resp = api_client_for_ui.create_board(board_name).get("id")

    board_page = BoardPage(browser)
    board_page.create_lists_for_moving(list_names)

    list_page = ListPage(browser)
    list_page.create_card(card_name)

    yield browser

    with allure.step("Удалить доску после теста"):
        api_client_for_ui.delete_board_by_id(resp) 


@pytest.fixture
def api_client() -> BoardAPI:
    with allure.step("Создать экземпляр класса BoardAPI"):
        return BoardAPI(
            ConfigProvider().get_api_url(),
            UserProvider().get_user_token())


@pytest.fixture
def api_client_no_auth() -> BoardAPI:
    with allure.step("Создать экземпляр класса BoardAPI без авторизации"):
        return BoardAPI(ConfigProvider().get("api", "base_url"), "")


@pytest.fixture
def dummy_board_id(api_client: BoardAPI, test_data: dict) -> str:
    card_name = test_data.get("card_name")
    with allure.step("Создать доску. Количество колонок по умолчанию - три"):
        resp = api_client.create_board(card_name).get("id")
        return resp


@pytest.fixture
def delete_board(api_client: BoardAPI) -> str:
    dictionary = {"board_id": ""}

    yield dictionary

    with allure.step("Получить id доски для её удаления"):
        board_id = dictionary.get("board_id")
    with allure.step("Удалить доску после теста"):
        api_client.delete_board_by_id(board_id)


@pytest.fixture
def dummy_board(api_client: BoardAPI, test_data: dict) -> str:
    card_name = test_data.get("card_name")
    with allure.step("Создать доску. Количество колонок по умолчанию - три"):
        resp = api_client.create_board(card_name).get("id")

        yield resp

    with allure.step("Удалить доску после теста"):
        api_client.delete_board_by_id(resp)    


@pytest.fixture
def lists_on_board(api_client: BoardAPI, dummy_board: str) -> dict:   
    lists_on_board = api_client.get_lists_by_board_id(dummy_board)

    with allure.step("Получить id колонок на доске"):    
        lists = {
            'list_one_id': lists_on_board[0]["id"],
            'list_two_id': lists_on_board[1]["id"],
            'list_three_id': lists_on_board[2]["id"]
        }
    with allure.step("перейти к удалению доски"):    
        yield lists  


@pytest.fixture
def api_card_client() -> CardAPI:
    with allure.step("Создать экземпляр класса CardAPI"):
        return CardAPI(
            ConfigProvider().get("api", "base_url"),
            UserProvider().get_user_token())


@pytest.fixture
def dummy_card_id(api_card_client: CardAPI, lists_on_board: dict, test_data: dict) -> str:
    list_one_id = lists_on_board['list_one_id']
    card_name = test_data.get("card_name")

    with allure.step("Создать карточку"):
        resp = api_card_client.create_card(list_one_id, card_name).get("id")

        return resp


@pytest.fixture
def get_lists_on_board_by_dummy_card_id(api_client: BoardAPI, api_card_client: CardAPI, dummy_card_id: str) -> dict:
    with allure.step("Получить id доски, на которой расположена карточка"):    
        board_id_of_card = api_card_client.get_card_info(dummy_card_id)["idBoard"]

    with allure.step("Получить список колонок на доске, на которой расположена карточка"):    
        lists_on_board = api_client.get_lists_by_board_id(board_id_of_card)    

    with allure.step("Получить id колонок на доске, на которой расположена карточка"):    
        lists = {
            'list_one_id': lists_on_board[0]["id"],
            'list_two_id': lists_on_board[1]["id"],
            'list_three_id': lists_on_board[2]["id"]
        }
        return lists