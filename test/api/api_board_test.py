from api.BoardApi import BoardApi
from faker import Faker


fake = Faker() 
org_id = "62a01eec169f028abfee19bd"
token = "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"
base_url = "https://trello.com/1/"
api = BoardApi(base_url, token)


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

    print("OLD NAME******** ", old_name)
    print("NEW NAME********", new_create_name)

    assert old_name != new_create_name
    

def test_delete_card(api_client: BoardApi, get_card_from_list: list, delete_board):
    old_list_cards_on_list = api_client.get_all_cards_on_list(get_card_from_list[3])

    api_client.delete_a_card(get_card_from_list[0])

    new_list_cards_on_list = api_client.get_all_cards_on_list(get_card_from_list[3])
    
    delete_board["board_id"] = get_card_from_list[2]

    print("old_list_cards_on_list---------", old_list_cards_on_list,  len(old_list_cards_on_list))
    print("new_list_cards_on_list---------", new_list_cards_on_list, len(new_list_cards_on_list))




