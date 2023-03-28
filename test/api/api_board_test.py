import allure
from api.BoardApi import BoardApi
from faker import Faker
import pytest

fake = Faker() 
org_id = "62a01eec169f028abfee19bd"
token = "62a01eb2f072a11c2e65969c/ATTScKZElxpOwaMptEcGVOzPa0nF8ZPh8aYXUP9CupnYn5iwrSvL60fqTSJD0yuEbTxYBEA745B5"
base_url = "https://trello.com/1/"
api = BoardApi(base_url, token)

# -------------------- Это начало эксперимента---------------------
@pytest.mark.skip
@allure.title("Тест на создание новой доски")
def test_create_board(api_client: BoardApi):
    with allure.step("Получить список всех досок учетной записи до создания доски"):
        board_list_before = api_client.get_all_boards_by_org_id(org_id)

    with allure.step("Создать доску"):
        resp = api_client.create_board(fake.company())     

    with allure.step("ПОлучить список всех досок учетной записи после создания доски"):
        board_list_after = api_client.get_all_boards_by_org_id(org_id)
    
    with allure.step("Удалить доску"):
        api_client.delete_board_by_id(resp.get("id"))

    with allure.step("Сравнить длины списков До и После"):
        assert len(board_list_after) - len(board_list_before) == 1



@pytest.mark.skip
@allure.title("Тест на удаление новй доски")
def test_delete_a_board(api_client: BoardApi, dummy_board_id:str):
    with allure.step("Получить список всех досок учетной записи до удаления доски"):
        board_list_before = api_client.get_all_boards_by_org_id(org_id)

    with allure.step("Удалить доску"):    
        api_client.delete_board_by_id(dummy_board_id)

    with allure.step("Получить список всех досок учетной записи после удаления доски"):
        board_list_after = api_client.get_all_boards_by_org_id(org_id)

    with allure.step("Сравнить длины списков До и После"):
        assert len(board_list_before) - len(board_list_after) == 1



@pytest.mark.skip   
@allure.title("Тест на создание карточки на доске")
def test_create_cadrd_on_board(api_client: BoardApi, get_id_list, delete_board): 
    with allure.step("Создать карточку на доске"):
        name_card = fake.text(20)
        resp = api_client.add_card(get_id_list[0], name_card)

    with allure.step("Получить id карточки"):
        id_create_card = resp["id"]

    with allure.step("Запросить имя карточки по её id"):
        get_name_card =api_client.get_card(id_create_card)["name"]

    with allure.step("Удалить доску по id"):
        delete_board["board_id"] = get_id_list[2]

    with allure.step("Сравнить присовенное имя и полученное по запросу"):
        assert name_card == get_name_card


    
@pytest.mark.skip
@allure.title("Переименование карточки")
def test_rename_card(api_client: BoardApi, create_new_card, delete_board):
    with allure.step("Запросить имя карточки до её редактирования"):
        get_name_card =api_client.get_card(create_new_card[0])["name"]

    with allure.step("переименовать карточку"):
        resp = api_client.rename_card(create_new_card[0])

    with allure.step("Запросить имя карточки после её  редактирования"):
        new_name_card =resp["name"]

    with allure.step("Удалить доску её id"):
        delete_board["board_id"] = create_new_card[2]

    with allure.step("Сравнить старое и новое имя"):
        assert get_name_card != new_name_card



@pytest.mark.skip
@allure.title("Удаление карточки")
def test_delete_card(api_client: BoardApi, create_new_card:list, delete_board):
    with allure.step("Запросить список карточек до удаления"):
        list_of_cards_before = api_client.get_all_cards_on_list(create_new_card[1])  # запрос всех карточек на листе

    with allure.step("Удалить карточку"):
        api_client.delete_a_card(create_new_card[0])

    with allure.step("ЗАпросить список карточек после удаления"):
        list_of_cards_after = api_client.get_all_cards_on_list(create_new_card[1])

    with allure.step("Удалить доску её id"):
        delete_board["board_id"] = create_new_card[2]

    with allure.step("Сравнить списки До и После"):
        assert len(list_of_cards_before) - len(list_of_cards_after) == 1


    
@pytest.mark.skip
@allure.title("Перенос карточки на другой список")
def test_relocate_card(api_client: BoardApi, create_new_card:list, get_id_list:dict, delete_board):
    with allure.step("Получить id карточки"):
        id_card = create_new_card[0]

    with allure.step("Получить id списка, на котором находится карточка"):
        id_old_list = get_id_list[0]

    with allure.step("Перенести карточку"):
        reloc = api_client.relocate_a_card(id_card, get_id_list[1])

    with allure.step("Получить id нового списка, на котором находится карточка"):
        id_new_list = reloc["idList"]

    with allure.step("Сравнить новый и старый id списков"):
        assert id_old_list != id_new_list

    with allure.step("Удалить доску"):
        delete_board["board_id"] = create_new_card[2]
    

# -------------------- Это окончание эксперимента---------------------
def test_get_all_boards(api_client: BoardApi):
    board_list = api_client.get_all_boards_by_org_id(org_id)
    id_board = board_list[0]["id"]
    api_client.delete_board_by_id(id_board)
