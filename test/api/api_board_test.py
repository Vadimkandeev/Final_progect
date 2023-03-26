import allure
from api.BoardApi import BoardApi
from faker import Faker


fake = Faker() 
org_id = "62a01eec169f028abfee19bd"
token = "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"
base_url = "https://trello.com/1/"
api = BoardApi(base_url, token)

# -------------------- Это начало эксперимента---------------------
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


def test_delete_a_board(api_client: BoardApi, dummy_board_id:str):
    with allure.step("Получить список всех досок учетной записи до удаления доски"):
        board_list_before = api_client.get_all_boards_by_org_id(org_id)
    with allure.step("Удалить доску"):    
        api_client.delete_board_by_id(dummy_board_id)
    with allure.step("Получить список всех досок учетной записи после удаления доски"):
        board_list_after = api_client.get_all_boards_by_org_id(org_id)
    with allure.step("Сравнить длины списков До и После"):
        assert len(board_list_before) - len(board_list_after) == 1
      

def test_create_cadrd_on_board(api_client: BoardApi, get_id_list:list):
    with allure.step("Создать карточку на доске"):
        name_card = fake.text(20)
        resp = api_client.add_card(get_id_list[0], name_card)
    with allure.step("Получить id карточки"):
        id_create_card = resp["id"]
    with allure.step("Запросить имя карточки по её id"):
        get_name_card =api_client.get_card(id_create_card)["name"]
    with allure.step("Сравнить присовенное имя и полученное"):
        assert name_card == get_name_card


def test_rename_card(api_client: BoardApi, create_new_card:list):
    with allure.step("Запросить имя карточки до её редактирования"):
        get_name_card =api_client.get_card(create_new_card[0])["name"]
    with allure.step("переименовать карточку"):
        resp = api_client.rename_card(create_new_card[0])
    with allure.step("Запросить имя карточки после её  редактирования"):
        new_name_card =resp["name"]
    with allure.step("Сравнить старое и новое имя"):
        assert get_name_card != new_name_card


def test_delete_card(api_client: BoardApi, create_new_card:list):
    with allure.step("Запросить список карточек до удаления"):
        list_of_cards_before = api_client.get_all_cards_on_list(create_new_card[1])  # запрос всех карточек на листе
    with allure.step("Удалить карточку"):
        api_client.delete_a_card(create_new_card[0])
    with allure.step("ЗАпросить список карточек после удаления"):
        list_of_cards_after = api_client.get_all_cards_on_list(create_new_card[1])
    with allure.step("Сравнить списки До и После"):
        assert len(list_of_cards_before) - len(list_of_cards_after) == 1
    


# -------------------- Это окончание эксперимента---------------------
"""
def test_create_board(api_client: BoardApi, delete_board:dict):
    board_list_before = api_client.get_all_boards_by_org_id(org_id)

    resp = api_client.create_board(fake.company())
    delete_board["board_id"] = resp.get("id")
    
    board_list_after = api_client.get_all_boards_by_org_id(org_id)
    assert len(board_list_after) - len(board_list_before) == 1
   



def test_delete_board(api_client: BoardApi, dummy_board_id: str):

    board_list_before = api_client.get_all_boards_by_org_id(org_id)
    
    api_client.delete_board_by_id(dummy_board_id)
    board_list_after = api_client.get_all_boards_by_org_id(org_id)
  
    assert len(board_list_before) - len(board_list_after) == 1


def test_create_new_card(api_client: BoardApi, get_list_from_a_board: list, delete_board): # , delete_board:dict
    
    note = fake.text(20)
    id_create_card = api_client.add_card(get_list_from_a_board[0], note)["id"]
    id_get_card =api_client.get_card(id_create_card)["id"]
    delete_board["board_id"] = get_list_from_a_board[1]
    # print ("id_create_card    ", id_create_card)
    # print ("id_get_card    ", id_get_card)
    # print ("get_list_from_a_board[1]    ", get_list_from_a_board[1])

    assert id_create_card == id_get_card


def test_rename_card (api_client: BoardApi, get_card_from_list: list, delete_board):
    old_name = get_card_from_list[1]
    new_create_name = api_client.rename_card(get_card_from_list[0])  
    delete_board["board_id"] = get_card_from_list[2]

    # print("OLD NAME******** ", old_name)
    # print("NEW NAME********", new_create_name)

    assert old_name != new_create_name
    

def test_delete_card(api_client: BoardApi, get_card_from_list: list, delete_board):
    old_list_cards_on_list = api_client.get_all_cards_on_list(get_card_from_list[3])

    api_client.delete_a_card(get_card_from_list[0])

    new_list_cards_on_list = api_client.get_all_cards_on_list(get_card_from_list[3])
    
    delete_board["board_id"] = get_card_from_list[2]

    # print("old_list_cards_on_list---------",  len(old_list_cards_on_list))
    # print("new_list_cards_on_list---------",  len(new_list_cards_on_list))

    assert len(old_list_cards_on_list) - len(new_list_cards_on_list) == 1


def test_relocate_a_card(api_client: BoardApi, get_card_from_list: list, delete_board):
    # relocate_a_card(self, id_card, id_board, id_new_list)
    id_card = get_card_from_list[0]
    print("id_card============", id_card)
    id_board = get_card_from_list[2]
    print("id_board===========", id_new_list)
    id_list = get_card_from_list[3]
    print("id_list============", id_list)
    id_new_list = get_card_from_list[4]
    print("id_new_list=======", id_new_list)
    api_client.relocate_a_card(id_card, id_board, id_new_list)
    print( api_client.get_list(id_new_list))

"""


